from Resto.models import Order
from Bakerys.models import OrderBakerys
import Resto
from django.db.models import Model
from django.utils.module_loading import import_module
from Resto.apps import RestoConfig
from django.apps import AppConfig


def get_app_name(self):

    return print(AppConfig.__name__)
   


    
    

   


    