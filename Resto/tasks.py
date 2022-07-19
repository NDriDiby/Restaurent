from urllib import request
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from celery.schedules import crontab
from .models import Order,Customer
from Restaurent.celery import app
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import OrderItem,Order
from django.db.models import F
from django.db.models import Max,Sum,Count
from datetime import datetime,timedelta,time
from django.utils import timezone
from urllib import request
import requests



today = timezone.localtime(timezone.now()).date()
TRANSFERT_RATE = 0.05


# Send Welcome Email
def welcomeEmail():
    subject = 'Bienvenu sur PINAV.CI'
    from_email = settings.EMAIL_HOST_USER
    to = 'prudencediby@gmail.com'
    html_content = render_to_string('Customer/welcomeEmail.html', {'context': 'values'})
    text_content = strip_tags(html_content)
    message = EmailMultiAlternatives(subject, text_content, from_email, [to])
    message.attach_alternative(html_content, "text/html")
    message.send()


@app.task
def add_number(x,y):
    return x+y



@shared_task
def send_paiement_receipt(order_id):
    order = Order.objects.get(id=order_id)
    subject = f"Commande: {order.transaction_id}"
    newline = "\n"
    message = f"Salut {order.customer.user.first_name},{newline}{newline}Votre commande est prete. Vous recevrez votre commande sous peu ci-dessous est votre reçu de commande.{newline}\
    {newline}Order Number: {order.transaction_id} \
    {newline}Order Total: {order.get_order_total()} FCFA\
    {newline}"

    
    return send_mail(subject,message,
    settings.EMAIL_HOST_USER,
    [order.customer.user.email],fail_silently=False,)
    
    
@shared_task
def get_daily_revenu():
    
    daily_rev = OrderItem.objects.filter(order__complete=True,order__date_ordered__date = today).select_related('item').values('item__name')\
    .annotate(my_sum= Sum(F("quantity")*F('item__prix')))
    total_daily_rev = daily_rev.aggregate(total_rev = Sum('my_sum'))
   
    return total_daily_rev['total_rev']

@shared_task
def transfert_amount():
    transfert_fees = get_daily_revenu() * TRANSFERT_RATE
    transfert = (get_daily_revenu()) - transfert_fees
    return transfert



# @shared_task
# def check_pending_order(table_number):
    
#     for tables in range(1,table_number):
#         order = Order.objects.all(status = 'Pending',table=tables)
#         print('My next order',order.date_ordered)
#         current_time = timezone.localtime(timezone.now())
#         if (order.date_ordered < current_time):
#             time_diff = (current_time - order.date_ordered)
#             print('it is been',round(time_diff.seconds/60))
#         if ((time_diff.seconds/60) >= 10):
#             order.delete()
#             print("ORDER DELETED")


@shared_task
def fetch_key():
    url = 'http://127.0.0.1:8000/cinetpayapi/'
    result = requests.get(url)
    result = result.json()
    apiKey = result['apiKey']
    site_id = result['site_id']
    return apiKey


@shared_task
def get_cinetpay_balance():
    #Get Token
    url ='https://client.cinetpay.com/v1/auth/login'
    data = {
        'apikey':fetch_key(),'password':"Goldenco901306$"
    }
    headers = {'Accept': 'application/x-www-form-urlencoded'}
    
    r = requests.post(url=url,
                     data=data,
                     headers=headers,
                     )
    result = r.json()['data']
    token = result['token']
    
  
    #Get Balance
    balance_url = 'https://client.cinetpay.com/v1/transfer/check/balance'
    data_balance ={
        'token':token,
    }
    balance = requests.get(url=balance_url,
                           params=data_balance)
    balance = balance.json()['data']
    
    return balance['amount']

@shared_task
def add_cinetpay_contact():
    
    url = 'https://client.cinetpay.com/v1/transfer/contact'
    headers = {'Accept': 'application/x-www-form-urlencoded'}
    
    data = {
    "prefix": "225",
    "phone": "01020304",
    "name": "Test A",
    "surname": "Test B",
    "email": "testa@exemple.com"
}
    
    r = requests.post(url = url,
                      headers=headers,
                      params= 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOjkzNTM2LCJpc3MiOiJodHRwczovL2NsaWVudC5jaW5ldHBheS5jb20vdjEvYXV0aC9sb2dpbiIsImlhdCI6MTY1NzI0NzgwMywiZXhwIjoxNjU3MjU1MDYzLCJuYmYiOjE2NTcyNDc4MDMsImp0aSI6IkhpbnV0bm0wMnpVZGlzQzUifQ.668aw_5JZ_zBfoZMg8I5JiNg8U_mK7PaamUU9hVhJ9w',
                      data=data
                      )
    
    result = r.json()
    return result
                        
    
    

    
    



        
