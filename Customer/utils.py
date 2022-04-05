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

    



    
   


    
    

   


    