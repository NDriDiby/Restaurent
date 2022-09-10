from cProfile import label
from cgitb import text
from itertools import count
from multiprocessing import context
import re
from xxlimited import new
import asgiref
from django.db import reset_queries
from django.forms import formset_factory
from django.shortcuts import render,redirect
from django.test import ignore_warnings
from django.urls import is_valid_path
from.models import (Accompagnement, Category,Customer,Item, ItemChoiceCategory,Order,OrderItem,ItemChoices,
                    IventoryItem,IventoryItemCategory,Transactions,SideOrderItem,Supplement)
from django.contrib import messages
from.forms import AddAccompForm, AddOptionCategoryForm, AddOptionForm, CustomerForm,ItemChoiceForm,AddProducts,AddItem,AddMenu,AddSupplementForm
from django.contrib.auth.models import User
import json
from Customer.utils import track_session,order_number,get_table_number,target_app,get_month
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http.response import HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import permission_required,login_required
import random
from datetime import datetime,timedelta,time
from django.utils import timezone
from django.db.models import F
from django.db.models import Max,Sum,Count
from django.conf import settings
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.forms.models import model_to_dict
from plotly.offline import plot
import plotly.express as px
import pandas as pd
import calendar
from dateutil.relativedelta import relativedelta
from django.forms.formsets import formset_factory
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

#TASK
from .tasks import (send_paiement_receipt,get_daily_revenu,
                    add_number,fetch_key,get_cinetpay_balance,add_cinetpay_contact)




 #App Name
app = Order._meta.app_label

today = timezone.localtime(timezone.now()).date()
yesterday = today - timedelta(days=1)
visit_number = None



#HomePage
# @permission_required('Resto.view_category')
def HomePage(request):
    
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    print(num_visits)
    
    popular_item = OrderItem.objects.values_list('item__name',flat=True).annotate(Quantity=Sum('quantity')).order_by('-Quantity')[:5]
    show_pop_item = Item.objects.filter(name__in=list(popular_item))
    
    #get_daily_revenu.delay()
    # fetch_key.delay()
    
    # get_cinetpay_balance.delay()
    
    # add_cinetpay_contact.delay()

    
    
    
    # add_number.delay(5,5)
    
    # for i in range(10,20):
    #     order = Order.objects.filter(status ='Pending',table=i)
    #     print('My next order',order)
    # for ord in order:
    #     current_time = timezone.localtime(timezone.now())
    #     if (order[ord].date_ordered < current_time):
    #         time_diff = (current_time - order[ord].date_ordered)
    #         print('it is been',round(time_diff.seconds/60))
    #     if ((time_diff.seconds/60) >= 10):
    #         order.delete()
    #         print("ORDER DELETED")
    
   
    
    #Table Number
    table = get_table_number(request)
    if table == None:
        pass
    
    
    
    # phone = request.GET.get('phone')
    # if phone == None:
    #     pass
    
    #Track user
    session = track_session(request)
    targetApp = target_app(request) #session=bakerys/?table=x
    
    
    order_sent = None #set order to none
    category = Category.objects.all().order_by("name") #Order the category by name
    sides = Accompagnement.objects.all()

    #After user has logged in
    if request.user.is_authenticated:
        #Create a customer object
        cust,created = Customer.objects.get_or_create(user =request.user)
        username = User.objects.get(id=request.user.id)
        cust.name = f'{username.first_name} {username.last_name}'
        # cust.phone = phone
        cust.save()
        
        
        
        #odd_even = Permission.objects.get(name='can_view_even_ids')
        
        if username.email == 'ndiby65@gmail.com':
            if username.has_perm("resto.view_iventory_item"):
                print("PERMISSONS")
            elif username.has_perm("resto.view_order"):
                print("I CAN SEE ORDERS")
            else:
                print('NO PERMISSIONS',username.email)
        # return HttpResponseRedirect(f'/noaccess/')
        else:
            print("NOT ME",username.email)
        
        #Show order to customer
        order_sent = Order.objects.filter(customer=cust, status = 'Sent', table =table, date_ordered__date = today).last()

        
    context = {
        'category':category,
        'order':order_sent,
        'app':targetApp,
        'side':sides,
        'show_pop_item':show_pop_item,
    }
    # return render(request,'Resto/HomePageNew.html',context)
    return render(request,'Resto/landingPage.html', context)


def UserProfile(request):
    
    cust,created = Customer.objects.get_or_create(user = request.user)
    
    all_order= Order.objects.filter(customer = cust,status='Completed')
    
    context = {
        'all_order':all_order,
    }
    
    return render(request,'Resto/user_profile.html',context)

#Menu Details
def MenuDetails(request,menu_id):
    
    
    #Get Table Number
    table = get_table_number(request)
    
    #Track user
    targetApp = target_app(request)

    #Get and show the item in each category
    menu = Category.objects.get(id = menu_id)
    category = Category.objects.all().order_by("name")
    item = Item.objects.filter(category__id = menu_id)
    sides = Accompagnement.objects.all()
    


    order = None
    cartItem = 0
    cartTotal = 0
    
    #Create customer and order
    
    # Authenticate then create an order
    if request.user.is_authenticated:
        try:
            username = User.objects.get(id=request.user.id)
            cust,created = Customer.objects.get_or_create(user =request.user)
            order,created= Order.objects.get_or_create(customer=cust,status='Pending',table=table)
            cartItem = order.get_order_quantity()
            cartTotal = order.get_order_total()
            
        
        except:
            pass
        
        
    context = {
        'menu':menu,
        'category':category,
        'item':item,
        'orders':order,
        'cart_quantity':cartItem,
        'cart_total':cartTotal,
        'app':targetApp,
        'sides':sides
        
    }
    return render(request,'Resto/MenuDetailsNew.html',context)


def SideDetails(request,side_id):
    
    
    #Get Table Number
    table = get_table_number(request)
    
    #Track user
    targetApp = target_app(request)

    #Get and show the item in each category
    side = Accompagnement.objects.get(id = side_id)
    side_items = Accompagnement.objects.exclude(id = side_id)
   
    
    order = None
    cartItem = 0
    cartTotal = 0
    
    
    # Authenticate then create an order
    if request.user.is_authenticated:
        try:
            username = User.objects.get(id=request.user.id)
            cust,created = Customer.objects.get_or_create(user =request.user)
            order,created= Order.objects.get_or_create(customer=cust,status='Pending',table=table)
            cartItem = order.get_order_quantity()
            cartTotal = order.get_order_total()
            my_total = order.get_order_total()
            
        except:
            pass
        
        
    context = {
        'side':side,
        'orders':order,
        'cart_quantity':cartItem,
        'cart_total':cartTotal,
        'app':targetApp,
        'my_total':my_total,
        'side_items':side_items,
    }
    return render(request,'Resto/sideDetails.html',context)

def MenuDetailsData(request,menu_id):
    
    #Get and show the item in each category
    menu = Category.objects.get(id = menu_id)
    category = Category.objects.all().order_by("name")
    item = Item.objects.filter(category__id = menu_id)
    
    print('All my Items',item)
    

    cat_item = list()
    for i in range(0,len(item)): 
        data = { 
                'item_id':item[i].id,
                'item_name':item[i].name,
                'item_description':item[i].description,
                'item_prix':item[i].prix,
                'item_img_url':item[i].img.url,
                'item_category_id':item[i].category.id,
                'item_category_name':item[i].category.name,
                'item_category_description':item[i].category.description,
                 'item_category_img_url':item[i].category.img.url,
                }
        cat_item.append(data)
    
    return JsonResponse({'item':cat_item,
                         'category':'cool'},safe=False)


def ItemDetails(request,item_id):
    
    #Item
    order = None
    cartItem = 0

    # supplement
    supplement = Supplement.objects.filter(item = item_id)

    #Get Table Number
    table = get_table_number(request)
    
    #Track user
    targetApp = target_app(request)
    
    
    item = Item.objects.get(id=item_id)
    my_item_accompID = [acc.id for acc in item.accompagnement.all()]
    side_item = Accompagnement.objects.exclude(id__in=my_item_accompID)
    
    
 
   
    cartItem = 0
    myItem = None
    my_total = 0
    show_pop_item=None
    item_cat_opt = None
    item_choice = None
    
    if request.user.is_authenticated:
        try:
            
            #Retrive the order
            cust,created = Customer.objects.get_or_create(user =request.user)
            order,created= Order.objects.get_or_create(customer=cust,status='Pending',table=table)
            cartItem = order.get_order_quantity()
            my_total = order.get_order_total()
            
            
            item_cat_opt = ItemChoiceCategory.objects.filter(item__id= item_id).order_by('name')
            item_choice = ItemChoices.objects.filter(parent_food = item_id)

           
            
         
        except:
            print('What wrong')
            pass
        
        #Check for past or pending order for the user
        pending_order = Order.objects.filter(customer=cust,status='Pending')
        print('DO I HAVE PENDING ORDER:',pending_order)
        if pending_order:
            for p in pending_order:
                if p.table != order.table:
                    print("you're on a new table")
                    pending_order.first().delete()
                    messages.warning(request,f"Vous ne pouvez pas passer de commande sur plusieurs tables")
                    messages.success(request,f"Votre nouveau numéro de table est {table}")
                    order= Order.objects.get_or_create(customer=cust,status='Pending',table=table)
                    print('a new table has been assign')
                    return HttpResponseRedirect(f'/homepage/?session={targetApp}')
            
    else:
        return HttpResponseRedirect(f'/register/?session={targetApp}')
        
    
    context = {
        'items':item,
        'orders':order,
        'cart_quantity':cartItem,
        'app':targetApp,
        'item_cat_opt':item_cat_opt,
        'item_choice': item_choice,
        # 'form':form,
        # 'assaisonement':assaisonement,
        # 'cuisson':cuisson,
        # 'ingredients':ingredients,
        # 'eau_mineral':eau_mineral,
        # 'coca_cola_produit':coca_cola_produit,
        'myitem':myItem,
        'my_total':my_total,
        'show_pop_item':show_pop_item,
        'supplements':supplement,
        'side_item':side_item,
    }
    
    return render (request,'Resto/ItemDetailsNew.html',context)
    

#My Order
def MyOrder(request):
    
    #Table Number
    table = get_table_number(request)
        

    #Track user
    targetApp = target_app(request)


    order = None
    items = None
    cartItem = 0
    order_id = 0


    #get the Order and  items
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created= Order.objects.get_or_create(customer=customer,status='Pending',table=table)
        items = order.orderitem_set.all()
        cartItem = order.get_order_quantity()
        side_item = order.sideorderitem_set.all()
        total_side_item = order.total_side_order_item()
        
       
       
        

        
    context = {
        'order':order,
        'items':items,
        'cart_quantity':cartItem,
        'side_items': side_item,
        'total_side_item':total_side_item,
        'app':targetApp
    }    
    return render(request,'Resto/myOrderNew.html',context)


#Backend Process of Item
def UpdatedItem(request):
    
    item_name = None
    total_cart = None
    tot_item= None
    total_accomp = 0
    tot_ind_item =0
    choice = None
    active_orderItem = None
    order_item_exist = False
    orderItem = None
  
    
    if request.method == 'POST':
        
        #Data from FrontEnd
        itemId = request.POST.get('itemId',False) #Item_id
        action = request.POST.get('action',False) #Add or remove
        choice = request.POST.get('choice',False) #Ingredient
        accompagment = request.POST.get('accomp',False) # Accompagement
        supplement = request.POST.get('sup',False) # Supplement
        side_itemId = request.POST.get('side_itemId',False) #Side_ItemID
        table_numb = int(request.POST['table']) #Table 
        
        
        

        
        
        #Retrieve Customer and Order
        customer = request.user
        customer,created= Customer.objects.get_or_create(user = request.user)
        order= Order.objects.get(customer=customer,status = 'Pending',table = table_numb)
        total = order.get_order_total()
        
       

        # If no Side Item ordered
        if side_itemId == False:
            
            
            # Find Choices
            choices = choice.split(',')
            my_choice = ItemChoices.objects.filter(name__in = choices)
            choice_id = [x.id for x in my_choice]
            print("NEXT",my_choice,choice_id)
           
            # Find Accompagnement
            acc = accompagment.split(",")
            my_acc = Accompagnement.objects.filter(name__in=acc)
            accomp_id_tuple = tuple([x.id for x in my_acc])
            accomp_id = [x.id for x in my_acc]
            
            
            #Find Supplement
            sup = supplement.split(",")
            my_sup = Supplement.objects.filter(name__in=sup)
            sup_id_tuple = tuple([x.id for x in my_sup])
            sup_id = [x.id for x in my_sup]
            print("the supplements checked are :", sup_id)
            
   
            # Find Item
            item = Item.objects.get(id=itemId)
            item_name = item.name
            
        
            #NO INGRE AND NO ACCOMP
            if not choice and not accompagment:
                
                if not supplement:  #If there is no supplement
                    print('NO INGRE AND ACCOMP AND SUP')
                    
                    #filter all order with no supplement
                    orderItem_all= OrderItem.objects.filter(customer=customer,order = order,item = item).all()
                    print('IS THERE ANY:',orderItem_all)
                    if not orderItem_all: #if there is nothing then create orderitem with no supplement
                        my_order_item= OrderItem.objects.create(customer=customer,order = order,item = item, quantity=1)
                        my_order_item.save()
                        tot_ind_item = my_order_item.quantity
                        tot_item = tot_ind_item
                        total = order.get_order_total()
                        active_orderItem = my_order_item.id
                        
                    
                    else: #if there are orderItem with supplement
                        for order_item in orderItem_all:
                            if not order_item.supplement.all(): #if no supplement is attached to the orderItem then we have our orderItem with no supplement
                                my_order_item = order_item
                                
                                if action =='add':
                                    my_order_item.quantity = (my_order_item.quantity + 1)
                                    my_order_item.save()
                                    tot_ind_item = my_order_item.quantity
                                    tot_item = tot_ind_item
                                    total = order.get_order_total()
                                    active_orderItem = my_order_item.id
                                    break
                            
                else: #If there is supplement
                   #find all orderitem that have a supplement
                    retrieve_order_item = OrderItem.objects.filter(customer=customer,order = order,item = item, supplement__in=sup_id).all()
                    if retrieve_order_item: # if we find an orderiten
                        for order_item in retrieve_order_item:
                            if set(order_item.supplement.all()) == set(my_sup): #check if it the same as the request from user
                                order_item_exist = True #then it is exist we have found our orderItem
                                my_order_item = OrderItem.objects.get(id = order_item.id)
                            
                                if action =='add':
                                    my_order_item.quantity = (my_order_item.quantity + 1)
                                    my_order_item.save()
                                    tot_ind_item = my_order_item.quantity
                                    tot_item = tot_ind_item
                                    total = order.get_order_total()
                                    active_orderItem = my_order_item.id
                                    break

                        if order_item_exist == False: #it is not the same as the user then create one
                            orderItem = OrderItem.objects.create(customer = customer,order = order, quantity =1)
                            orderItem.supplement.add(*sup_id_tuple)
                            orderItem.item = item 
                            orderItem.save()
                            tot_ind_item = 1
                            total = order.get_order_total()
                    else:
                        orderItem= OrderItem.objects.create(customer = customer,order = order, quantity =1)
                        orderItem.supplement.add(*sup_id_tuple)
                        orderItem.item = item 
                        orderItem.save()
                        tot_ind_item = 1
                        total = order.get_order_total()
               
                
            #ONLY INGRE
            if choice and not accompagment:
                if not supplement: # if there is supplement
                    #find all order with no supplement but with ingredient
                    retrieve_orderItem_all= OrderItem.objects.filter(customer=customer,order = order,item = item, ingredient__in = choice_id).all()
                    print("What do I have:",retrieve_orderItem_all)
                    if retrieve_orderItem_all: #if there is nothing then create one
                        for order_item in retrieve_orderItem_all:
                            if(set(order_item.ingredient.all()) == set(my_choice) and not order_item.supplement.all()):
                                order_item_exist = True
                                my_order_item = OrderItem.objects.get(id = order_item.id)
                                
                                if action =='add':
                                    my_order_item.quantity = (my_order_item.quantity + 1)
                                    my_order_item.save()
                                    tot_ind_item = my_order_item.quantity
                                    tot_item = tot_ind_item
                                    total = order.get_order_total()
                                    active_orderItem = my_order_item.id
                                    break
                        
                        if order_item_exist == False:
                            orderItem= OrderItem.objects.create(customer=customer,order = order,quantity=1)
                            orderItem.ingredient.add(*tuple(choice_id))
                            orderItem.item = item
                            orderItem.save()
                            tot_ind_item = 1
                            total = order.get_order_total()
                                  
                    else: #if there is some
                        orderItem= OrderItem.objects.create(customer=customer,order = order,quantity=1)
                        orderItem.ingredient.add(*tuple(choice_id))
                        orderItem.item = item
                        orderItem.save()
                        tot_ind_item = 1
                        total = order.get_order_total()
                            
                        
                else: #if there supplement
                    
                    #filter all order with ingredient and supplement
                    retrieve_orderItem_all= OrderItem.objects.filter(customer=customer,order = order,item = item, ingredient__in = choice_id, supplement__in = my_sup).all()
                    if retrieve_orderItem_all: # if there is one 
                        for order_item in retrieve_orderItem_all:
                            if (set(order_item.supplement.all()) == set(my_sup) and set(order_item.ingredient.all()) == set(my_choice)): #check if it the same as the user request
                                order_item_exist = True #if true we have our orderItem
                                my_order_item = OrderItem.objects.get(id = order_item.id)
                        
                                if action =='add':
                                    my_order_item.quantity = (my_order_item.quantity + 1)
                                    my_order_item.save()
                                    tot_ind_item = my_order_item.quantity
                                    tot_item = tot_ind_item
                                    total = order.get_order_total()
                                    active_orderItem = my_order_item.id
                                    break
                            
                        if order_item_exist == False: # if is not the same as the user request then create a orderitem
                            orderItem = OrderItem.objects.create(customer = customer,order = order, quantity=1)
                            orderItem.supplement.add(*sup_id_tuple)
                            orderItem.ingredient.add(*tuple(choice_id))
                            orderItem.item = item 
                            orderItem.save()
                            tot_ind_item = 1
                            total = order.get_order_total()
                    else:
                        orderItem = OrderItem.objects.create(customer = customer,order = order, quantity=1)
                        orderItem.supplement.add(*sup_id_tuple)
                        orderItem.ingredient.add(*tuple(choice_id))
                        orderItem.item = item 
                        orderItem.save()
                        tot_ind_item = 1
                        total = order.get_order_total()
                            
                    
                
            # #ONLY ACCOMP
            if accompagment and not choice:
                print('THIS MY ACCOMP_NAME:',accompagment)
                if not supplement:  #if there is no supplement
                    #Find all order with and accompagement
                    retrieve_order_item = OrderItem.objects.filter(customer=customer,order=order,item = item,accompagnememt__in=accomp_id)
                    if retrieve_order_item: #if there is an item
                        for order_item in retrieve_order_item: #Check if it is the accompagement are the same as the user request
                            if (set(order_item.accompagnememt.all()) == set(my_acc) and not order_item.supplement.all()): #if is true 
                                order_item_exist = True #then we have our item
                                my_order_item = OrderItem.objects.get(id = order_item.id)
        
                                if action =='add':
                                    my_order_item.quantity = (my_order_item.quantity + 1)
                                    my_order_item.save()
                                    tot_ind_item = my_order_item.quantity
                                    tot_item = tot_ind_item
                                    total = order.get_order_total()
                                    active_orderItem = my_order_item.id
                                break
                            
                        if order_item_exist == False: #if not the same as the user request then create an orderItem
                            orderItem = OrderItem.objects.create(customer = customer,order = order, quantity =1)
                            orderItem.accompagnememt.add(*accomp_id_tuple)
                            orderItem.item = item 
                            orderItem.save()
                            tot_ind_item = 1
                            total = order.get_order_total()
                            
                    else:
                        orderItem= OrderItem.objects.create(customer = customer,order = order, quantity =1)
                        orderItem.accompagnememt.add(*accomp_id_tuple)
                        orderItem.item = item 
                        orderItem.save()
                        tot_ind_item = 1
                        total = order.get_order_total()   
                        
                else: #if there is a supplement
                    #find all order with accompagement and supplement
                    retrieve_order_item = OrderItem.objects.filter(customer=customer,order=order,item = item,accompagnememt__in=accomp_id, supplement__in = sup_id)
                    if retrieve_order_item: #if there is one
                        for order_item in retrieve_order_item: #check if the orderItem correspond to the user request
                            if (set(order_item.accompagnememt.all()) == set(my_acc) and set(order_item.supplement.all()) == set(my_sup)):
                                order_item_exist = True #if it is true then we have found our orderItem
                                my_order_item = OrderItem.objects.get(id = order_item.id)
                                
                                if action =='add':
                                    my_order_item.quantity = (my_order_item.quantity + 1)
                                    my_order_item.save()
                                    tot_ind_item = my_order_item.quantity
                                    tot_item = tot_ind_item
                                    total = order.get_order_total()
                                    active_orderItem = my_order_item.id
                                break
                            
                        if order_item_exist == False: #if it is the same as the user request then create one
                            orderItem = OrderItem.objects.create(customer = customer,order = order, quantity =1)
                            orderItem.accompagnememt.add(*accomp_id_tuple)
                            orderItem.supplement.add(*sup_id_tuple)
                            orderItem.item = item 
                            orderItem.save()
                            tot_ind_item = 1
                            total = order.get_order_total()
                    else:
                        orderItem = OrderItem.objects.create(customer = customer,order = order, quantity =1)
                        orderItem.accompagnememt.add(*accomp_id_tuple)
                        orderItem.supplement.add(*sup_id_tuple)
                        orderItem.item = item 
                        orderItem.save()
                        tot_ind_item = 1
                        total = order.get_order_total()
                                
            
                    

            # #ACCOMP + INGRE
            if accompagment and choice:
                print('ACCOMP + INGRE')
                if not supplement:
                    print("ORDER ITEM WITH NO SUPPLEMENT")
                    retrieve_order_item = OrderItem.objects.filter(customer=customer,order=order,item = item, ingredient__in = choice_id,accompagnememt__in=accomp_id)
                    if retrieve_order_item:
                        for order_item in retrieve_order_item:
                            if (set(order_item.accompagnememt.all()) == set(my_acc) and set(order_item.ingredient.all()) == set(my_choice)) and not order_item.supplement.all():
                                order_item_exist = True
                                my_order_item = OrderItem.objects.get(id = order_item.id)
                                print("I FOUND YOU")

                                if action =='add':
                                    print('I ADDED +1')
                                    my_order_item.quantity = (my_order_item.quantity + 1)
                                    my_order_item.save()
                                    tot_ind_item = my_order_item.quantity
                                    tot_item = tot_ind_item
                                    total = order.get_order_total()
                                    active_orderItem = my_order_item.id
                                    break
                        
                        if order_item_exist == False:
                            print('I DID NOT FOUND YOU, I WILL CREATE ONE')
                            orderItem = OrderItem.objects.create(customer = customer,order = order, quantity =1)
                            orderItem.accompagnememt.add(*accomp_id_tuple)
                            orderItem.item = item
                            orderItem.ingredient.add(*tuple(choice_id))
                            orderItem.save()
                            tot_ind_item = 1
                            total = order.get_order_total()
                    else:
                        print('I DID NOT FOUND YOU, I WILL CREATE ONE')
                        orderItem = OrderItem.objects.create(customer = customer,order = order, quantity =1)
                        orderItem.accompagnememt.add(*accomp_id_tuple)
                        orderItem.item = item
                        orderItem.ingredient.add(*tuple(choice_id))
                        orderItem.save()
                        tot_ind_item = 1
                        total = order.get_order_total()
                        
                else: 
                    retrieve_order_item = OrderItem.objects.filter(customer=customer,order=order,item = item, ingredient__in = choice_id,accompagnememt__in=accomp_id, supplement__in = sup_id)
                    if retrieve_order_item:
                        for order_item in retrieve_order_item:
                            if ( set(order_item.accompagnememt.all()) == set(my_acc) and set(order_item.ingredient.all()) == set(my_choice)   and  set(order_item.supplement.all()) == set(my_sup)):
                                order_item_exist = True
                                my_order_item = OrderItem.objects.get(id = order_item.id)
                                
                                if action =='add':
                                    print('I ADDED +1')
                                    my_order_item.quantity = (my_order_item.quantity + 1)
                                    my_order_item.save()
                                    tot_ind_item = my_order_item.quantity
                                    tot_item = tot_ind_item
                                    total = order.get_order_total()
                                    active_orderItem = my_order_item.id
                                break
                        
                        if order_item_exist == False:
                            orderItem= OrderItem.objects.create(customer = customer,order = order, quantity =1)
                            orderItem.accompagnememt.add(*accomp_id_tuple)
                            orderItem.supplement.add(*sup_id_tuple)
                            orderItem.item = item
                            orderItem.ingredient.add(*tuple(choice_id))
                            orderItem.save()
                            tot_ind_item = 1
                            total = order.get_order_total()
                            
                    else:
                        print("LETS START HERE")
                        orderItem= OrderItem.objects.create(customer = customer,order = order, quantity =1)
                        orderItem.accompagnememt.add(*accomp_id_tuple)
                        orderItem.supplement.add(*sup_id_tuple)
                        orderItem.item = item
                        orderItem.ingredient.add(*tuple(choice_id))
                        orderItem.save()
                        tot_ind_item = 1
                        total = order.get_order_total()
                        
         
            item_selected = list()
            item = order.orderitem_set.all()
            for i in range(0,len(item)): 
                data = { 
                        'orderItem_id':item[i].id,
                        'order_id':item[i].order.id,
                        'description':item[i].item.description,
                        # 'order':order[i].customer.user.first_name +" "+ order[i].customer.user.last_name,
                        'item':item[i].item.name,
                        'quantity':item[i].quantity,
                        # 'ingredient':item[i].ingredient,
                        'total':item[i].get_total(),
                        'item_price':item[i].item.prix,
                        'item_price_item':item[i].get_total_item(),
                        'total_item_accomp':item[i].get_total_accomp(),
                        }
                item_selected.append(data)
                
        else:
            sideItem = Accompagnement.objects.get(id = side_itemId)
            sideOrderItem,created = SideOrderItem.objects.get_or_create(customer = customer, order = order, item = sideItem)
            item_name = sideItem.name
            
            if action =='add':
                    sideOrderItem.quantity = (sideOrderItem.quantity + 1)
                    sideOrderItem.save()
                    tot_ind_item = sideOrderItem.quantity
                    total = order.get_order_total()
                    tot_item = tot_ind_item
                    active_orderItem = sideOrderItem.id
                    item_selected = 'Okay'
            
           
        total_cart = order.get_order_quantity()
            
            
    return JsonResponse({"item_name":item_name,
                        'total_cart':total_cart,
                        'tot_item':tot_item,
                        'tot_ind_item':tot_ind_item,
                        'total':total,
                        'orderItem':item_selected,
                        'active_orderItem':active_orderItem,
                        'total_accomp':total_accomp,
                        'test':10}
                        ,safe=False)


def CheckoutPageUpdate(request):
    
    item_name = None
    total_cart = None
    tot_item= None
    total_item = 0
    total_accomp = 0
    tot_ind_item =0
    choice = None
    active_orderItem = None
    order_item_exist = False
    total_order_item = 0
    total_sup = 0
    
    if request.POST:
        
        #Get Data from frontend
        orderItemID = request.POST.get('ordItem',False) #OrderItem ID
        sideorderitem = request.POST.get('sideorderitem',False) #SideItem ID
        table_numb = int(request.POST.get('table')) #Table
        action = request.POST.get('action',False) #Add or remove
        
       
    
        #retrieve the OrderItem
        customer,created= Customer.objects.get_or_create(user = request.user)
        order= Order.objects.get(customer=customer,status = 'Pending',table = table_numb)
       
        
        if orderItemID:
            my_order_item = OrderItem.objects.get(id = orderItemID)
            
            
            if action =='add':
                my_order_item.quantity = (my_order_item.quantity + 1)
                my_order_item.save()

            
            if action =='remove':
                my_order_item.quantity = (my_order_item.quantity - 1)
                my_order_item.save()
                
            tot_ind_item = my_order_item.quantity
            total_item = my_order_item.get_total_item()
            total_order_item = my_order_item.get_total()
            total_sup = my_order_item.get_total_accomp()
            active_orderItem = my_order_item.id
    
        else:
            my_order_item = SideOrderItem.objects.get(id = sideorderitem)
            
            if action =='add':
                my_order_item.quantity = (my_order_item.quantity + 1)
                my_order_item.save()
            
            if action =='remove':
                my_order_item.quantity = (my_order_item.quantity - 1)
                my_order_item.save()
            
            total_item = my_order_item.quantity
            tot_ind_item = my_order_item.quantity
            active_orderItem = my_order_item.id
            total_order_item = my_order_item.total_side_order()
            orderItemID = sideorderitem
        
        item_name = my_order_item.item.name
        total_cart = order.get_order_total()
        total = order.get_order_total()
        
        
    return JsonResponse({"order_item_id":orderItemID,
                        'total_cart':total_cart,
                        'tot_ind_item':tot_ind_item,
                        'total':total,
                        'total_item':total_item,
                        'active_orderItem':active_orderItem,
                        'total_order_item':total_order_item,
                        'total_supplement':total_sup,
                        'item_name':item_name}
                        ,safe=False)



def GetOrderCuisine(request):
    
    #Uncompleted Order
    uncompleted_order = Order.objects.filter(status='Sent',date_ordered__date = today).order_by('date_ordered')
    completed_order = Order.objects.filter(complete=True,date_ordered__date = today).order_by('-date_ordered')
        
    
    current_time = datetime.strftime(datetime.today().now(),'%H:%M')
    current_time= datetime.strptime(current_time,'%H:%M')
    
    uncompleted = list()
    for order in range(0,len(uncompleted_order)):
        
        order_date = datetime.strftime(uncompleted_order[order].date_ordered,'%H:%M')
        #order_date= datetime.strptime(order_date,'%H:%M')
        
        #time_since = current_time - order_date
        data = {
            'order_id':uncompleted_order[order].id,
            'order_table':uncompleted_order[order].table,
            'order_name':uncompleted_order[order].customer.full_name(),
            'order_date':order_date,
            'transaction_id':uncompleted_order[order].transaction_id,
            'order_item':[],
            'side_orderitem':[],
        }
        
        # data['order_date'] = datetime.strftime(data['order_date'],'%H:%M')
        #datetime.strftime(uncompleted_order[order].date_ordered,'%H:%M')
        # print('DateOrdered:',current_time)
        # print('DateOrdered_since:',time_since)
        # print(order_date)
        
        #ORDER ITEM
        all_orderitem = uncompleted_order[order].orderitem_set.all()
        for orderitem in range(0,len(all_orderitem)):
            if data['order_id'] == all_orderitem[orderitem].order.id:
                orderItem = {
                   'order_id':all_orderitem[orderitem].order.id,
                    'orderItem_id':all_orderitem[orderitem].id,
                   'order':all_orderitem[orderitem].customer.user.first_name +" "+ all_orderitem[orderitem].customer.user.last_name,
                    'item':all_orderitem[orderitem].item.name,
                    'quantity':all_orderitem[orderitem].quantity,
                }
                
                if all_orderitem[orderitem].ingredient:
                    for ingre in all_orderitem[orderitem].ingredient.all():
                        orderItem['ingredient'] = list(all_orderitem[orderitem].ingredient.values_list('name',flat = True))
                    
                if all_orderitem[orderitem].accompagnememt:
                    for accomp in all_orderitem[orderitem].accompagnememt.all():
                        orderItem['accompagnement'] = list(all_orderitem[orderitem].accompagnememt.values_list('name',flat=True))
                        
                if all_orderitem[orderitem].supplement:
                    for sup in all_orderitem[orderitem].supplement.all():
                        orderItem['supplement'] = list(all_orderitem[orderitem].supplement.values_list('name',flat=True))
                        
                       
                data['order_item'].append(orderItem)
        
        # SIDE ORDER ITEM
        if uncompleted_order[order].sideorderitem_set.all():
            all_side = uncompleted_order[order].sideorderitem_set.all()
            for side in range(0,len(all_side)):
                if data['order_id'] == all_side[side].order.id:
                    my_side = {
                        'order_id':all_side[side].order.id,
                        'name':all_side[side].item.name,
                        'quantity':all_side[side].quantity,
                    }
            
                    data['side_orderitem'].append(my_side)
        uncompleted.append(data)
        
        
    completed = list()
    for order in range(0,len(completed_order)):
        
        order_date = datetime.strftime(completed_order[order].date_completed,'%H:%M')
        #order_date= datetime.strptime(order_date,'%H:%M')
        
        #time_since = current_time - order_date
        data = {
            'order_id':completed_order[order].id,
            'order_table':completed_order[order].table,
            'order_name':completed_order[order].customer.full_name(),
            'order_date_completed':order_date,
            'transaction_id':completed_order[order].transaction_id,
            'order_item':[],
            'side_orderitem':[],
        }
        
        # data['order_date'] = datetime.strftime(data['order_date'],'%H:%M')
    #    datetime.strftime(uncompleted_order[order].date_ordered,'%H:%M')
        # print('DateOrdered:',current_time)
        # print('DateOrdered_since:',time_since)
        # print(order_date)
        
        #ORDER ITEM
        all_orderitem = completed_order[order].orderitem_set.all()
        for orderitem in range(0,len(all_orderitem)):
            if data['order_id'] == all_orderitem[orderitem].order.id:
                orderItem = {
                   'order_id':all_orderitem[orderitem].order.id,
                    'orderItem_id':all_orderitem[orderitem].id,
                   'order':all_orderitem[orderitem].customer.user.first_name +" "+ all_orderitem[orderitem].customer.user.last_name,
                    'item':all_orderitem[orderitem].item.name,
                    'quantity':all_orderitem[orderitem].quantity,
                }
                
                if all_orderitem[orderitem].ingredient:
                    for ingre in all_orderitem[orderitem].ingredient.all():
                        orderItem['ingredient'] = list(all_orderitem[orderitem].ingredient.values_list('name',flat = True))
                    
                if all_orderitem[orderitem].accompagnememt:
                    for accomp in all_orderitem[orderitem].accompagnememt.all():
                        
                        orderItem['accompagnement'] = list(all_orderitem[orderitem].accompagnememt.values_list('name',flat=True))
                        
                if all_orderitem[orderitem].supplement:
                    for sup in all_orderitem[orderitem].supplement.all():
                        orderItem['supplement'] = list(all_orderitem[orderitem].supplement.values_list('name',flat=True))
                        
                       
                data['order_item'].append(orderItem)
        
        # SIDE ORDER ITEM
        if completed_order[order].sideorderitem_set.all():
            all_side = completed_order[order].sideorderitem_set.all()
            for side in range(0,len(all_side)):
                if data['order_id'] == all_side[side].order.id:
                    my_side = {
                        'order_id':all_side[side].order.id,
                        'name':all_side[side].item.name,
                        'quantity':all_side[side].quantity,
                    }
            
                    data['side_orderitem'].append(my_side)
        completed.append(data)
    
  
    return JsonResponse({"uncompleted_order":list(uncompleted),
                         "completed_order":list(completed)})
                         


def Cuisine(request):
    
    uncompleted_order = Order.objects.filter(status='Sent',date_ordered__date = today)
    completed_order = Order.objects.filter(complete=True,date_completed__date = today).order_by('date_completed')
    
    # total_completed_order = len(complete_order)
    # total_uncompleted_order = len(uncompleted_order)
    
   
    
    context ={
        'all_order':uncompleted_order,
         'total_completed_order':uncompleted_order.count,
         'completed_order':completed_order,
         'uncompleted_order':uncompleted_order,
    }
    
    return render(request,"Resto/MyCuisine.html",context)


@csrf_exempt
def CompletedOrder(request):
    
    if request.method == 'POST':
        order_numb = request.POST.get('id')
        order = Order.objects.get(id = order_numb)
        item = order.orderitem_set.all()
        order.status = 'Completed'
        order.complete = True
        order.date_completed = timezone.localtime()
        order.save()
        
        uncompleted_order = Order.objects.filter(status='Sent',date_ordered__date = today).count()
    
        # #TASK
        # send_paiement_receipt.delay(order_numb)
        

    return JsonResponse({'response':"Order Completed",
                         'uncompleted_order':uncompleted_order},safe=False)


#BackEnd process of Order
def SendOrder(request):
    
    customer = request.user
    order = Order.objects.filter(customer__id = customer.customer.id).last()
    total_item = order.get_order_quantity()
    item_selected = list()
    item = order.orderitem_set.all()
    for i in range(0,len(item)): 
        data = { 
                'orderItem_id':item[i].id,
                'order_id':item[i].order.id,
                'description':item[i].item.description,
                #'order':order[ord].customer.user.first_name +" "+ order[ord].customer.user.last_name,
                'item':item[i].item.name,
                'quantity':item[i].quantity,
                # 'ingredient':item[i].ingredient,
                }
        item_selected.append(data)
    
    
    
    #get the data from the BackEnd
    if request.method == 'POST':
        action = request.POST['action']
        order_numb = request.POST['order']

        customer = request.user
        cust,created = Customer.objects.get_or_create(user =request.user)
        order,created = Order.objects.get_or_create(id=order_numb, customer = cust)
        icarus_img = '/static/Resto/Icarus.png'

    
        #Process the order
        item = order.get_order_quantity()
        if item >0:
            order.status = 'Sent'
            order.transaction_id = order_number('NovaCloud')
            order.save()
            
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                "uncompleted-order",
                {
                    'type':'order_status',
                    'message': order.id
                }
            )
            
        return JsonResponse({'Order_Status':'Sent to kitchen','icarus_img':icarus_img})
            
            

    return JsonResponse({'order':10,'total_item':total_item,'orderItem':item_selected})


#Cuisine (Owner access Only)
@login_required
@permission_required('Resto.view_order',login_url='/login/') #Permission required
def DashBoard(request):
    
    #Order of the day
    #Show all order sent to the kitchen
    all_order = Order.objects.filter(status='Sent',date_ordered__date = today)
    complete_order = Order.objects.filter(complete=True,date_completed__date = today).order_by('date_completed')
    
    #Show all order sent to the kitchen yesterday
    all_order_ystd = Order.objects.filter(status='Sent',date_ordered__date = yesterday)
    complete_order_ystd = Order.objects.filter(complete=True,date_completed__date = yesterday).order_by('date_completed')
    
    
    
    #Top 5 Meals
    orderItem = list(OrderItem.objects.values('item__name','item__category__name').annotate(Quantity=Sum('quantity')).order_by('-Quantity')[:5])
    print(list(orderItem))
    
    
    #viz Top 5 meals
    # df = pd.DataFrame(orderItem)
    # fig = px.bar(df,x='item__name', y='Quantity',color='item__category__name',text_auto='Quantity',
    #              color_discrete_sequence=['bisque','crimson', 'turquoise','green','darkgreen'],opacity=0.7)
    # plt = plot(fig,output_type='div')
    
    # # continuous
    # ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
    #          'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
    #          'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
    #          'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
    #          'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
    #          'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
    #          'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
    #          'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
    #          'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
    #          'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
    #          'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar',
    #          'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
    #          'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid',
    #          'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
    #          'ylorrd']
    
    # #descrete
    # # [aliceblue, antiquewhite, aqua, aquamarine, azure,
    # #         beige, bisque, black, blanchedalmond, blue,
    # #         blueviolet, brown, burlywood, cadetblue,
    # #         chartreuse, chocolate, coral, cornflowerblue,
    # #         cornsilk, crimson, cyan, darkblue, darkcyan,
    # #         darkgoldenrod, darkgray, darkgrey, darkgreen,
    # #         darkkhaki, darkmagenta, darkolivegreen, darkorange,
    # #         darkorchid, darkred, darksalmon, darkseagreen,
    # #         darkslateblue, darkslategray, darkslategrey,
    # #         darkturquoise, darkviolet, deeppink, deepskyblue,
    # #         dimgray, dimgrey, dodgerblue, firebrick,
    # #         floralwhite, forestgreen, fuchsia, gainsboro,
    # #         ghostwhite, gold, goldenrod, gray, grey, green,
    # #         greenyellow, honeydew, hotpink, indianred, indigo,
    # #         ivory, khaki, lavender, lavenderblush, lawngreen,
    # #         lemonchiffon, lightblue, lightcoral, lightcyan,
    # #         lightgoldenrodyellow, lightgray, lightgrey,
    # #         lightgreen, lightpink, lightsalmon, lightseagreen,
    # #         lightskyblue, lightslategray, lightslategrey,
    # #         lightsteelblue, lightyellow, lime, limegreen,
    # #         linen, magenta, maroon, mediumaquamarine,
    # #         mediumblue, mediumorchid, mediumpurple,
    # #         mediumseagreen, mediumslateblue, mediumspringgreen,
    # #         mediumturquoise, mediumvioletred, midnightblue,
    # #         mintcream, mistyrose, moccasin, navajowhite, navy,
    # #         oldlace, olive, olivedrab, orange, orangered,
    # #         orchid, palegoldenrod, palegreen, paleturquoise,
    # #         palevioletred, papayawhip, peachpuff, peru, pink,
    # #         plum, powderblue, purple, red, rosybrown,
    # #         royalblue, rebeccapurple, saddlebrown, salmon,
    # #         sandybrown, seagreen, seashell, sienna, silver,
    # #         skyblue, slateblue, slategray, slategrey, snow,
    # #         springgreen, steelblue, tan, teal, thistle, tomato,
    # #         turquoise, violet, wheat, white, whitesmoke,
    # #         yellow, yellowgreen]
    

    # Total order of the day
    total_completed_order = complete_order.count()
    total_uncompleted_order = all_order.count()
    total_order = total_completed_order + total_uncompleted_order
    
    # # Total order from the yesteray day
    # total_completed_order_ystd = complete_order_ystd.count()
    # total_uncompleted_order_ystd = all_order_ystd.count()
    # total_order_ystd = total_completed_order + total_uncompleted_order
    
    # #Total customer
    total_customer = Customer.objects.distinct().count()
    # print("MY CUST",total_customer)
    
    # #Order in an hour
    # orderHour = Order.objects.filter(date_ordered__date = today).values('date_ordered__hour').annotate(count_order=Count('id'))
    # print(orderHour)
    # plt2 = "There is upcoming order"
    # if orderHour:
    #     df2 = pd.DataFrame(orderHour)
    #     fig2 = px.line(df2,x='date_ordered__hour', y='count_order',markers=True,text='count_order',
    #                 color_discrete_sequence=['crimson', 'turquoise','green','darkgreen'])
        
    #     fig2.update_traces(textposition="bottom right")
    #     fig2.update_xaxes(
    #     rangeslider_visible=False,
    #     rangeselector=dict(
    #         buttons=list([
    #             dict(count=1, label="1h", step="hour", stepmode="backward"),
    #             dict(count=6, label="6m", step="month", stepmode="backward"),
    #             dict(count=1, label="YTD", step="year", stepmode="todate"),
    #             dict(count=1, label="1y", step="year", stepmode="backward"),
    #             dict(step="all")
    #         ])
    #     )
    # )
    #     plt2 = plot(fig2,output_type='div')
        
    
    # print("TOTAL  ORDER",total_order,total_completed_order_ystd)
    # print("TOTAL COMP ORDER",total_completed_order,total_completed_order_ystd)
    
    # print(complete_order_ystd)
   
   
    
    
    context = {
        'all_order':all_order,
        'complete':complete_order,
        'total_completed_order':total_completed_order,
        'total_uncompleted_order':total_uncompleted_order,
        'total_order':total_order,
        # 'vizTop5meals':plt,
        # 'vizOrder':plt2,
        'today':today,
        'visit':visit_number,
        'total_customer':total_customer,
        'orderitem':orderItem,
        
    }
    return render(request,'Resto/Icarus_dashboard.html',context)



#Backend process
def DeleteItem(request):
    
    #Get the item then delete
    if request.method == 'POST':
        item_id = request.POST['item_id']
        del_items = Item.objects.get(id =item_id)
    
    return JsonResponse('item deleted',safe=False)

#Backend Process
def DeleteOrderItem(request):
    
    if request.method == 'POST':
        order_item_id = request.POST['item_id']
        try:
            del_items = OrderItem.objects.get(id = order_item_id)
            del_items.delete()
        except:
            del_items = SideOrderItem.objects.get(id = order_item_id)
            del_items.delete()
        
    return JsonResponse('item deleted',safe=False)



#Inventory Management System
@login_required
@permission_required('Resto.view_inventory_item',login_url='/login/') #Permission required
def Recipe(request):
    my_items =  Item.objects.all().order_by('name')
    
    
   
   
    if request.method == 'POST':
        form_cat = AddMenu(request.POST,request.FILES or None)
        form_accomp = AddAccompForm(request.POST,request.FILES or None)
        form = AddItem(request.POST,request.FILES or None)
        form_sup = AddSupplementForm(request.POST,request.FILES or None)
        form_opt_cat = AddOptionCategoryForm(request.POST,request.FILES or None)
        form_opt = AddOptionForm(request.POST,request.FILES or None)
        
           
        
        product_cat = request.POST.get('category',None)
        product_name = request.POST.get('prod_name',None)
        product_prix = request.POST.get('prod_prix',None)
        product_des = request.POST.get('description',None)
        product_img = request.FILES.get('prod_img',None)
        product_accomp = request.POST.getlist('accompagnement',None)
        product_sup = request.POST.getlist('supplement',None)
        print(product_cat,product_name,product_prix,product_des,product_img,product_accomp,product_sup)
        if product_name:
            if product_name.lower() in [item.name.lower() for item in my_items]:
                print('this Iitem already exit')
                messages.info(request,f'{product_name} already exist')
                return HttpResponseRedirect(f'/recipe/')
            else:
                prod_cat = Category.objects.get(id = product_cat)
                prod = Item.objects.create(
                    name = product_name,
                    prix = product_prix,
                    description = product_des,
                    img = f'images/{product_img}',
                    category = prod_cat,
                )
                prod.accompagnement.add(*tuple(product_accomp))
                prod.supplement_set.add(*tuple(product_sup))
                prod.save()
                messages.success(request,f'{product_name} created')
                print('I got the data')
                return HttpResponseRedirect(f'/recipe/')
            
            
          #Cat
        cat_name= request.POST.get('cat_name',None)
        if cat_name:
            if cat_name.lower() in [c.name.lower() for c in Category.objects.all()]:
                messages.info(request,f'{cat_name} already exist')
                return HttpResponseRedirect(f'/recipe/')
            else:
                cat = Category.objects.create(
                    name = cat_name,
                )
                cat.save()
                messages.success(request,f'{cat_name} created')
                print('I got the data')
                return HttpResponseRedirect(f'/recipe/')
            
         #Sup
        sup_name= request.POST.get('sup_name',None)
        sup_prix = request.POST.get('sup_prix',None)
        if sup_name:
            if sup_name.lower() in [sup.name.lower() for sup in Supplement.objects.all()]:
                messages.info(request,f'{sup_name} already exist')
                return HttpResponseRedirect(f'/recipe/')
            else:
                supp = Supplement.objects.create(
                    name = sup_name,
                    prix = sup_prix,
                )
                supp.save()
                messages.success(request,f'{sup_name} created')
                print('I got the data')
                return HttpResponseRedirect(f'/recipe/')
            
        
        #Accomp
        accomp_name= request.POST.get('accomp_name',None)
        accomp_prix = request.POST.get('accomp_prix',None)
        accomp_img = request.POST.get('img',None)
        if accomp_name:
            if accomp_name.lower() in [acc.name.lower() for acc in Accompagnement.objects.all()]:
                messages.info(request,f'{accomp_name} already exist')
                return HttpResponseRedirect(f'/recipe/')
            else:
                acc = Accompagnement.objects.create(
                    name = accomp_name,
                    prix = accomp_prix,
                    img = f'images/{accomp_img}'
                )
                acc.save()
                messages.success(request,f'{accomp_name} created')
                print('I got the data')
                return HttpResponseRedirect(f'/recipe/')
        
        
        #Opt
        option_name= request.POST.get('cat_opt_name',None)
        option_recette = request.POST.getlist('item',None)
        option_multi = request.POST.get('multiple_choice',None)
        option_cat = request.POST.get('category_opt',None)
        
        
        
        if option_multi == 'on':
            option_multi = True
        else:
             option_multi = False
             
        if option_name:
            if option_name.lower() in [opt.name.lower() for opt in ItemChoiceCategory.objects.all()]:
                messages.info(request,f'{option_name} already exist')
                return HttpResponseRedirect(f'/recipe/')
            else:
                opt_cat = ItemChoiceCategory.objects.create(
                    name = option_name,
                    multiple_choice = option_multi
                )
                opt_cat.item.add(*tuple(option_recette))
                opt_cat.save()
                messages.success(request,f'{option_name} created')
                print('I got the data')
                return HttpResponseRedirect(f'/recipe/')  
            
        if  option_cat:
                option_name = ItemChoiceCategory.objects.get(id=option_cat)
                option_name.item.add(*tuple(option_recette))
                option_name.save()
                messages.success(request,f'{option_name} created')
                print('I got the data')
                return HttpResponseRedirect(f'/recipe/')
            
            
    else:
        form = AddItem()
        form_cat = AddMenu()
        form_accomp = AddAccompForm()
        form_sup = AddSupplementForm()
        form_opt_cat = AddOptionCategoryForm()
        form_opt = AddOptionForm()

    context = {
        'form':form,
        'form_accomp':form_accomp,
        'form_cat':form_cat,
        'items':my_items,
        'form_sup':form_sup,
        'form_opt_cat': form_opt_cat,
        'form_opt':form_opt,
    }
    
    return render(request,'Resto/items_cuisine.html',context)


#Backend Process
def Recette(request):
    
    if request.method == 'POST':
        action = request.POST.get('action',None)
        
        if action == 'accomp':
            item = request.POST.get('item',None)
            name = request.POST.get('accomp_name',None)
            prix = request.POST.get('accomp_prix',None)
            img = request.POST.get('accomp_img',None)
            accomp_id = request.POST.get('accomps',None)
           
            # New Accomp
            if name:
                if name.lower() in [acc.name.lower() for acc in Accompagnement.objects.all()]:
                    return JsonResponse({'message':'exist'})
                else:
                    new_acc = Accompagnement.objects.create(
                        name = name,
                        prix = prix,
                        img = f'images/{img}')
                    new_acc.save()
                    my_item = Item.objects.get(id=item)
                    my_item.accompagnement.add(new_acc)
                    my_item.save()
                    return JsonResponse({'message':'added'})
                
            # Existing Accomp
            if accomp_id:
                print('My Accomp',accomp_id)
                my_item = Item.objects.get(id=item)
                my_accomp = accomp_id.split(',')
                my_accomp_id = [int(x) for x in my_accomp]
                accomp = Accompagnement.objects.filter(id__in=my_accomp_id)
                all_accomp = [a.id for a in my_item.accompagnement.all()]
                print('ALL',all_accomp)
                for acc in my_accomp_id:
                    if acc in all_accomp:
                       return JsonResponse({'message':'exist'})
                    else:
                        my_item.accompagnement.add(*tuple(my_accomp_id))
                        my_item.save()
                        return JsonResponse({'message':'added'})
                
                
        # New Sup
        if action == 'sup':
            item = request.POST.get('item')
            name = request.POST.get('sup_name')
            prix = request.POST.get('sup_prix')
            sup_id = request.POST.get('sups',None)
            
            if name:
                if name.lower() in [sup.name.lower() for sup in Supplement.objects.all()]:
                    return JsonResponse({'message':'exist'})
                else:
                    my_item = Item.objects.get(id=item)
                    new_sup = Supplement.objects.create(
                        name = name,
                        prix = prix)
                    new_sup.item.add(my_item)
                    new_sup.save()
                return JsonResponse({'message':'added'})
            
            
            
            # Existing Sup
            if sup_id:
                my_item = Item.objects.get(id=item)
                my_sup = sup_id.split(',')
                my_sup_id = [int(x) for x in my_sup]
                my_sup = Supplement.objects.filter(id__in=my_sup_id)
                sup_id = [x.id for x in my_item.supplement_set.all()]
                for s in my_sup_id:
                    if s in sup_id:
                        return JsonResponse({'message':'exist'})
                    else:
                        my_item.supplement_set.add(*tuple(my_sup_id))
                        return JsonResponse({'message':'added'})
        
        
        # Option
        if action == 'opt':
           option_name = request.POST.get('opt_name',None)
           opt_cat_id = request.POST.get('opt_cat',None)
           opt_recette = request.POST.get('receipe',None)
           old_choice_id = request.POST.get('old_choice',None)
           
           print(option_name,opt_cat_id,opt_recette)
           recette = opt_recette.split(',')
           recette_id = [int(x) for x in recette]
           print(recette_id)
           opt_cat = ItemChoiceCategory.objects.get(id = opt_cat_id)
           opt_cat_name = opt_cat.name
           
           
           
           if option_name:
               if option_name.lower() in [x.name.lower() for x in ItemChoices.objects.all()]:
                    return JsonResponse({'message':'exist','choice':option_name})
               
               else:
                   
                   re = ItemChoiceCategory.objects.get(id = opt_cat_id)
                   if re:
                        re.item.add(*tuple(recette_id))
                        re.save()
                        add_opt = ItemChoices.objects.create(name =  option_name,choice_category = re, prix = 0)
                        add_opt.parent_food.add(*tuple(recette_id))
                        add_opt.save()
                   else:
                        re = ItemChoiceCategory.objects.create(name = opt_cat_name, prix = 0)
                        re.item.add(*tuple(recette_id))
                        re.save()
                        add_opt = ItemChoices.objects.create(name =  option_name,choice_category = re, prix = 0)
                        add_opt.parent_food.add(*tuple(recette_id))
                        add_opt.save()
                    
          
           if old_choice_id:
               add_opt = ItemChoices.objects.get(id = old_choice_id )
               add_opt.parent_food.add(*tuple(recette_id))
               add_opt.save()

           return JsonResponse({'message': 'added','choice':add_opt.name})
       
       
    return JsonResponse({'ready for action':'?'})


def Settings(request):
    categories = IventoryItemCategory.objects.all()
    
    
    if request.method == 'POST':
        
        form = AddItem(request.POST,request.FILES or None)
        form_menu = AddMenu(request.POST,request.FILES or None)
        
        if form.is_valid():
            item = form.cleaned_data.get('name')
            category = form.cleaned_data.get('category')
            print('I got the data')
            #form.save()
            # messages.success(request,f'{item} added to your recette list')
            # return HttpResponseRedirect(f'/texasgrillz/settings/')
            
    else:
        form = AddItem()
        form_menu = AddMenu()

    context = {
        'categorie': categories,
        'form':form,
        'form_menu':form_menu
    }
    
    return render(request,'Resto/CuisineSettings.html',context)



def Analytics(request):
    
    #Top 5 Meals
    orderItem = OrderItem.objects.filter(date_added__date = today).values('item__name','item__category__name')\
        .annotate(Quantity=Sum('quantity')).order_by('-Quantity')[:5]
        
    plt = None
    revPerMenuPlot = None
        
    if orderItem:
        df = pd.DataFrame(orderItem)
        fig = px.bar(df,x='item__name', y='Quantity',color='item__category__name',text_auto='Quantity',
                    color_discrete_sequence=['bisque','crimson', 'turquoise','green','darkgreen'],opacity=0.7)
        plt = plot(fig,output_type='div')
    
    #REVENU OF THE DAY PER MENU
    revPerMenu = OrderItem.objects.filter(order__complete=True,date_added__date = today).select_related('item','item__category__name').values('item__category__name')\
        .annotate(my_sum = Sum(F("quantity")*F('item__prix')))
    revPerMonthPlot = 'There is no item'
    
    if revPerMenu:
        df = pd.DataFrame(revPerMenu)
        fig = px.pie(df,names='item__category__name', values='my_sum',hover_data=['my_sum'],
                    color_discrete_sequence=['bisque','crimson', 'turquoise','green','darkgreen'],opacity=0.7)
        fig.update_traces(textposition='inside', textinfo='percent+value')
        revPerMenuPlot = plot(fig,output_type='div')
    
    
    #REVENUE PER MONTH
    revPerMonth = OrderItem.objects.filter(order__complete=True,date_added__date__month__lte = today.month).select_related('item').values('date_added__date__month')\
        .annotate(my_sum= Sum(F("quantity")*F('item__prix')))
    df = pd.DataFrame(revPerMonth)
    get_month(df)
    df = df.rename({'date_added__date__month':'Mois','my_sum':'Total'},axis=1)
  
    fig2 = px.bar(df,x='Mois', y='Total',hover_data=['Total'],text_auto='Total',
                 color_discrete_sequence=['bisque','crimson', 'turquoise','green','darkgreen'],opacity=0.7
                 )
    fig2.update_traces(textposition='inside')
    revPerMonthPlot = plot(fig2,output_type='div')
    
    #Revenu per Month
    complete_order = Order.objects.filter(complete=True,date_completed__date__month = today.month).order_by('date_completed')
    revMonth = [sum(x.get_order_total() for x in complete_order)]
    
    #Revenu per Day
    complete_order_day = Order.objects.filter(complete=True,date_completed__date = today).order_by('date_completed')
    revDay = [sum(x.get_order_total() for x in complete_order_day)]
    
    
    #Order in an Month
    orderMonth = Order.objects.filter(date_ordered__date__month__lte = today.month).values('date_ordered__month').annotate(count_order=Count('id'))
    print(orderMonth)
    plt2 = "There is upcoming order"
    if orderMonth:
        df2 = pd.DataFrame(orderMonth)
        get_month(df2)
        fig2 = px.line(df2,x='date_ordered__month', y='count_order',markers=True,text='count_order',
                    color_discrete_sequence=['crimson', 'turquoise','green','darkgreen'])
        
        fig2.update_traces(textposition="bottom right")
        fig2.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1h", step="hour", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )
        plt2 = plot(fig2,output_type='div')
        
    
    
        
    
    context = {
        'vizTop5meals':plt,
        'revPerMenuPlot':revPerMenuPlot,
        'revPerMonthPlot':revPerMonthPlot,
        'vizOrderMonth':plt2,
        'revMonth':revMonth[0],
        'revDay':revDay[0],
        
    }
    
    return render(request, 'Resto/Analytics.html',context)


def Revenues(request):
    
    complete_order = Order.objects.filter(complete=True,date_completed__date = today).order_by('date_completed')
    total = [sum(x.get_order_total() for x in complete_order)]
    revPerMenuPlot = None
    
    #REVENU OF THE DAY PER MENU
    revPerMenu = OrderItem.objects.filter(order__complete=True,date_added__date = today).select_related('item','item__category__name').values('item__category__name')\
        .annotate(my_sum = Sum(F("quantity")*F('item__prix')))
    
    if revPerMenu:
        df = pd.DataFrame(revPerMenu)
        fig = px.pie(df,names='item__category__name', values='my_sum',hover_data=['my_sum'],
                    color_discrete_sequence=['bisque','crimson', 'turquoise','green','darkgreen'],opacity=0.7)
        fig.update_traces(textposition='inside', textinfo='percent+value')
        revPerMenuPlot = plot(fig,output_type='div')
    
    
    #REVENUE PER MONTH
    revPerMonth = OrderItem.objects.filter(order__complete=True,date_added__date__month__lte = today.month).select_related('item').values('date_added__date__month')\
        .annotate(my_sum= Sum(F("quantity")*F('item__prix')))
        
    if revPerMonth:
        df = pd.DataFrame(revPerMonth)
        get_month(df)
        df = df.rename({'date_added__date__month':'Mois','my_sum':'Total'},axis=1)
    
        fig2 = px.bar(df,x='Mois', y='Total',hover_data=['Total'],text_auto='Total',
                    color_discrete_sequence=['bisque','crimson', 'turquoise','green','darkgreen'],opacity=0.7)
        fig2.update_traces(textposition='inside')
        revPerMonthPlot = plot(fig2,output_type='div')
    
    
    
    
    
    context = {
        'monthRev':total[0],
        'revPerMenuPlot':revPerMenuPlot,
        'revPerMonthPlot':revPerMonthPlot,
    }
    
    return render(request, 'Resto/Revenues.html',context)

#Backend Process
def ProcessTransaction(request):
    if request.method == 'POST':
        user = Customer.objects.get(user = request.user)
        
        #Transaction info
        amount = request.POST.get('amount')
        orderID = request.POST.get('orderID')
        currency = request.POST.get('currency')
        description = request.POST.get('description')
        operator_id = request.POST.get('operator_id')
        payment_date = request.POST.get('payment_date')
        status = request.POST.get('status')
        transactionID = request.POST.get('transactionID')
        payment_method = request.POST.get('payment_method')
    
        #Appointement Info
        # object = request.POST.get('objet')
        # date = request.POST.get('date')
        
        
        print('working fine, just ckecking',[user, orderID,payment_method,
        amount,currency,description,operator_id,
        payment_date,status,transactionID])
        
        
        #Record Transaction
        record_trans,created = Transactions.objects.get_or_create(
        user = user,
        # order = orderID,
        amount =  amount,
        currency =  currency ,
        description =  description,
        operator_id =    operator_id ,
        payment_date =  payment_date,
        status =  status ,
        transactionID = transactionID,
        payment_method =  payment_method,
        )
        
        record_trans.save()
        
        print('END OF TRANSACTION')
        
    return JsonResponse({'valider':status})

def CinetPayCredential(request):
    
    apikey = "188254710627a7eefc41627.61387840"
    site_id = "722116"
    
    
    return JsonResponse({'apiKey':apikey,'site_id':site_id})


#TASKS + JOBS
def DashBoardData(request):
    
    my_items =  Item.objects.all().order_by('prix')
    recette = my_items.count()
    
    uncompleted_order = Order.objects.filter(status='Sent',date_ordered__date = today).count()
    complete_order = Order.objects.filter(complete=True,date_completed__date = today).order_by('date_completed').count()
    
    daily_rev = OrderItem.objects.filter(order__complete=True,order__date_ordered__date = today).select_related('item').values('item__name')\
    .annotate(my_sum= Sum(F("quantity")*F('item__prix')))
    total_daily_rev = daily_rev.aggregate(total_rev = Sum('my_sum'))
    
    all_items = list()
    for item in range(0,len(my_items)):
        data ={
             'name': my_items[item].name,
              'prix': my_items[item].prix,
              'category': my_items[item].category.name,
              'accompagnement': [],
              'supplement':[],
            #   'date_created': my_items[item].date_created,
        }
        all_items.append(data)
        
        
        accomp = my_items[item].accompagnement.all()
        if accomp:
            for acc in range(0,len(accomp)):
                    my_accomp = {
                        'accomp_name': accomp[acc].name,
                    }
                    data['accompagnement'].append(my_accomp)
       
       
        sup = Supplement.objects.filter(item__id = my_items[item].id)
        if sup:
            for s in range(0,len(sup)):
                my_sup = {
                    'sup_name':sup[s].name
                }
                data['supplement'].append(my_sup)
                
       
        
    
    orderItem = list(OrderItem.objects.values('item__name','item__category__name').annotate(Quantity=Sum('quantity')).order_by('-Quantity')[:5])
    orderHour = list(Order.objects.filter(date_ordered__date = today).values('date_ordered__hour').annotate(count_order=Count('id')))
    
      #REVENU OF THE DAY PER MENU
    revPerMenu = list(OrderItem.objects.filter(order__complete=True,date_added__date = today).select_related('item','item__category__name').values('item__category__name')\
        .annotate(my_sum = Sum(F("quantity")*F('item__prix'))))
    
    #REVENUE PER MONTH
    revPerMonth = list(OrderItem.objects.filter(order__complete=True,date_added__date__month__lte = today.month).select_related('item').values('date_added__date__month')\
        .annotate(my_sum= Sum(F("quantity")*F('item__prix'))))
    
    return JsonResponse({'dashboard':orderItem,
                         'ordertime':orderHour,
                         'my_items':all_items,
                         'revPerMenu':revPerMenu,
                         'revPerMonth':revPerMonth,
                         'uncompleted_order':uncompleted_order,
                         'completed_order':complete_order,
                         'recette':recette,
                         'total_rev':total_daily_rev
                         })
    
    