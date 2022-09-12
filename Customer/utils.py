from Resto.models import Order
import Resto
from django.db.models import Model
from django.utils.module_loading import import_module
from Resto.apps import RestoConfig
from django.apps import AppConfig
from django.conf import settings
from django.urls import resolve
from random import randint


# from urllib import request
# from celery import shared_task
# from django.core.mail import send_mail
# from django.conf import settings
# from celery.schedules import crontab
# from .models import Order,Customer
# from Restaurent.celery import app
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from .models import OrderItem,Order
# from django.db.models import F
# from django.db.models import Max,Sum,Count
# from datetime import datetime,timedelta,time
# from django.utils import timezone
# from urllib import request
# import requests



# today = timezone.localtime(timezone.now()).date()
# TRANSFERT_RATE = 0.05


# # Send Welcome Email
# def welcomeEmail():
#     subject = 'Bienvenu sur PINAV.CI'
#     from_email = settings.EMAIL_HOST_USER
#     to = 'prudencediby@gmail.com'
#     html_content = render_to_string('Customer/welcomeEmail.html', {'context': 'values'})
#     text_content = strip_tags(html_content)
#     message = EmailMultiAlternatives(subject, text_content, from_email, [to])
#     message.attach_alternative(html_content, "text/html")
#     message.send()


# @app.task
# def add_number(x,y):
#     return x+y



# @shared_task
# def send_paiement_receipt(order_id):
#     order = Order.objects.get(id=order_id)
#     subject = f"Commande: {order.transaction_id}"
#     newline = "\n"
#     message = f"Salut {order.customer.user.first_name},{newline}{newline}Votre commande est prete. Vous recevrez votre commande sous peu ci-dessous est votre reçu de commande.{newline}\
#     {newline}Order Number: {order.transaction_id} \
#     {newline}Order Total: {order.get_order_total()} FCFA\
#     {newline}"

    
#     return send_mail(subject,message,
#     settings.EMAIL_HOST_USER,
#     [order.customer.user.email],fail_silently=False,)
    
    
# @shared_task
# def get_daily_revenu():
    
#     daily_rev = OrderItem.objects.filter(order__complete=True,order__date_ordered__date = today).select_related('item').values('item__name')\
#     .annotate(my_sum= Sum(F("quantity")*F('item__prix')))
#     total_daily_rev = daily_rev.aggregate(total_rev = Sum('my_sum'))
   
#     return total_daily_rev['total_rev']

# @shared_task
# def transfert_amount():
#     transfert_fees = get_daily_revenu() * TRANSFERT_RATE
#     transfert = (get_daily_revenu()) - transfert_fees
#     return transfert


#Tracking user 
def track_session(request):
    """ this function will track the current user on the web browser"""
    session = None
    if 'session' in request.GET:
        session = request.GET.get('session').lower()
    return session


def order_number(session):
    ''' This function create andom number for orders'''
    number = [str(randint(0,9)) for i in range(0,5)]
    letter = [ sess.upper() for sess in session ]
    letter = "".join(letter)
    number = "".join(number)
    order_number = letter+' #'+str(number)
    return order_number


def target_app(request):
    ''' This function track the session and the table number '''
    try:
        session_id = request.GET.get('session')
        table = request.GET.get('table')
        phone = request.GET.get('phone')
        connected = request.GET.get('connected')

        if session_id == None or table == None:
            targetApp = 'nosession'
        else:
            targetApp = session_id+'&table='+table
            
        return targetApp
    except:
        pass


def get_table_number(request):
    ''' This function retrive the table number '''
    try:
        table = str(request.GET.get('table'))
        if table == None:
            pass
        else:
            table = str(request.GET.get('table'))
            if table is not None:
                table = int(table)
            return table
    except:
        pass
    
    
def get_month(df):
    for i in range(0,len(df)):
        if df.iloc[i,0] == 1:
            df.iloc[i,0] = 'Janvier'
        elif df.iloc[i,0] == 2:
            df.iloc[i,0] = 'Fevrier'
        elif df.iloc[i,0] == 3:
            df.iloc[i,0] = 'Mars'
        elif df.iloc[i,0] == 4:
            df.iloc[i,0] = 'Avril'
        elif df.iloc[i,0] == 5:
            df.iloc[i,0] = 'Mai'
        elif df.iloc[i,0] == 6:
            df.iloc[i,0] = 'Juin'
        elif df.iloc[i,0] == 7:
            df.iloc[i,0] = 'Juiellet'
        elif df.iloc[i,0] == 8:
            df.iloc[i,0] = 'Aout'
        elif df.iloc[i,0] == 9:
            df.iloc[i,0] = 'Septembre'
        elif df.iloc[i,0] == 10:
            df.iloc[i,0] = 'October'
        elif df.iloc[i,0] == 11:
            df.iloc[i,0] = 'Novembre'
        elif df.iloc[i,0] == 12:
            df.iloc[i,0] = 'December'
    return df


    



    
   


    
    

   


    