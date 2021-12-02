from Resto.models import Order
from Bakerys.models import OrderBakerys
import Resto
from django.db.models import Model
from django.utils.module_loading import import_module
from Resto.apps import RestoConfig
from django.apps import AppConfig
from django.conf import settings
from django.urls import resolve
from random import randint



#Tracking user 
def track_session(request):

    """ this function will track the current user on the web browser"""

    session = None
    if 'session' in request.GET:
        session = request.GET.get('session').lower()
    return session

def order_number():
    number = [str(randint(0,9)) for i in range(0,5)]
    letter = ['B','A','K','E','R','Y','S']
    letter = "".join(letter)
    number = "".join(number)
    order_number = letter+' #'+str(number)
    return order_number



    
   


    
    

   


    