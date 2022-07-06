from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from celery.schedules import crontab
from .models import Order




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