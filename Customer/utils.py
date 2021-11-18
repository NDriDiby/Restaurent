from Resto.models import Order
from Bakerys.models import OrderBakerys
import Resto
from django.db.models import Model
from django.utils.module_loading import import_module
from Resto.apps import RestoConfig
from django.apps import AppConfig
from django.conf import settings
from django.urls import resolve


#Tracking user 
def track_session(request):

    """ this function will track the current user on the web browser"""

    session = None
    if 'session' in request.GET:
        session = request.GET.get('session').lower()
    return session

    
   


    
    

   


    