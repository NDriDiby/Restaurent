from cProfile import label
from cgitb import text
from itertools import count
from multiprocessing import context
import re
from django.db import reset_queries
from django.shortcuts import render,redirect
from django.test import ignore_warnings
from.models import (Accompagnement, Category,Customer,Item,Order,OrderItem,ItemChoices,
                    IventoryItem,IventoryItemCategory, SideOrderItem, Supplement,Transactions)
from django.contrib import messages
from.forms import CustomerForm,ItemChoiceForm,AddProducts,AddItem,AddMenu
from django.contrib.auth.models import User
import json
from Customer.utils import track_session,order_number,get_table_number,target_app,get_month
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http.response import HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import permission_required,login_required
import random
from datetime import datetime,timedelta,time
from django.utils import timezone
from Bakerys.forms import OrderForm
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
        'side':sides
    }
    return render(request,'Resto/HomePageNew.html',context)


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


#Menu Details
def SideDetails(request,side_id):
    
    
    #Get Table Number
    table = get_table_number(request)
    
    #Track user
    targetApp = target_app(request)

    #Get and show the item in each category
    side = Accompagnement.objects.get(id = side_id)
    # category = Category.objects.all().order_by("name")
    # item = Item.objects.filter(category__id = menu_id)
    # sides = Accompagnement.objects.all()
    


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
            my_total = order.get_order_total()
            
        
        except:
            pass
        
        
    context = {
        # 'menu':menu,
        # 'category':category,
        'side':side,
        'orders':order,
        'cart_quantity':cartItem,
        'cart_total':cartTotal,
        'app':targetApp,
        'my_total':my_total,
        
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

    #Form
    form = ItemChoiceForm()
    form.base_fields['name'].queryset = ItemChoices.objects.filter(parent_food_id = item_id,choice_category__name__icontains= 'Assaisonement')
    
    #Choice Category
    assaisonement = ItemChoices.objects.filter(parent_food_id= item_id, choice_category__name__icontains= 'assaisonement')
    cuisson = ItemChoices.objects.filter(parent_food_id= item_id, choice_category__name__icontains= 'cui')
    ingredients = ItemChoices.objects.filter(parent_food_id= item_id, choice_category__name__icontains= 'ingredients')
    eau_mineral = ItemChoices.objects.filter(parent_food_id= item_id, choice_category__name__icontains= 'eau mineral')
    coca_cola_produit = ItemChoices.objects.filter(parent_food_id= item_id, choice_category__name__icontains= 'coca-cola')
    supplement = Supplement.objects.filter(item = item_id)
    
    
    print("EXTRA",supplement.all())
    

    #Get Table Number
    table = get_table_number(request)
    
    #Track user
    targetApp = target_app(request)
    
    
    item = Item.objects.get(id=item_id)
    
   
    cartItem = 0
    myItem = None
    my_total = 0
    show_pop_item=None
    
    if request.user.is_authenticated:
        try:
            #Retrive the order
            cust,created = Customer.objects.get_or_create(user =request.user)
            order,created= Order.objects.get_or_create(customer=cust,status='Pending',table=table)
            cartItem = order.get_order_quantity()
            my_total = order.get_order_total()
            
            
            
            popular_item = OrderItem.objects.values_list('item__name',flat=True).annotate(Quantity=Sum('quantity')).order_by('-Quantity')[:5]
            show_pop_item = Item.objects.filter(name__in=list(popular_item))
            
            
            
            #Check for past or pending order for the user
            pending_order = Order.objects.filter(customer=cust,status='Pending')
            if len(pending_order) > 1:
                pending_order.delete()
                messages.warning(request,"Vous ne pouvez pas passer de commande sur plusieurs tables")
                messages.success(request,f"Votre nouveau numéro de table est {table}")
                order,created= Order.objects.get_or_create(customer=cust,status='Pending',table=table)
                return HttpResponseRedirect(f'/texasgrillz/?session={targetApp}')
            
            
                
        except:
            pass
            
    
    else:
        return HttpResponseRedirect(f'/register/?session={targetApp}')
        
    
    context = {
        'items':item,
        'orders':order,
        'cart_quantity':cartItem,
        'app':targetApp,
        'form':form,
        'assaisonement':assaisonement,
        'cuisson':cuisson,
        'ingredients':ingredients,
        'eau_mineral':eau_mineral,
        'coca_cola_produit':coca_cola_produit,
        'myitem':myItem,
        'my_total':my_total,
        'show_pop_item':show_pop_item,
        'supplements':supplement
        
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
        

        
    context = {
        'order':order,
        'items':items,
        'side_items': side_item,
        'cart_quantity':cartItem,
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
    accomp = None
    choice = None
    active_orderItem = None
    order_item_exist = False
  
    
    
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
                print('NO INGRE AND ACCOMP')
               
                if not supplement:  #If there is no supplement
                    #filter all order with no supplement
                    orderItem_all= OrderItem.objects.filter(customer=customer,order = order,item = item,ingredient = None).all()
                    if not orderItem_all: #if there is nothing then create orderitem with no supplement
                        orderItem= OrderItem.objects.create(customer=customer,order = order,item = item, ingredient = None)
                    
                    else: #if there are orderItem with supplement
                        for item in orderItem_all:
                            if not item.supplement.all(): #if no supplement is attached to the orderItem then we have our orderItem with no supplement
                                orderItem = item
                                break
                                
                    if action =='add':
                        orderItem.quantity = (orderItem.quantity + 1)
                        orderItem.save()
                        tot_ind_item = orderItem.quantity
                        total = order.get_order_total()
                        # my_order_item = OrderItem.objects.filter(order= order, item = item)
                        # tot_item = [sum(x.quantity for x in my_order_item)][0]
                        tot_item = tot_ind_item
                        active_orderItem = orderItem.id
                    
               
                else: #If there is supplement
                   #find all orderitem that have a supplement
                    retrieve_order_item = OrderItem.objects.filter(customer=customer,order = order,item = item, ingredient = None, supplement__in=sup_id).all()
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
                    retrieve_orderItem_all= OrderItem.objects.filter(customer=customer,order = order,item = item, ingredient = choice).all()
                    if not retrieve_orderItem_all: #if there is nothing then create one
                        orderItem= OrderItem.objects.create(customer=customer,order = order,item = item, ingredient = choice)
                    else: #if there is some
                        for item in retrieve_orderItem_all: #Check if there is a supplement
                            if not item.supplement.all(): #if not then we have our order
                                orderItem = item
                                break
                        
                    if action =='add':
                        orderItem.quantity = (orderItem.quantity + 1)
                        orderItem.save()
                        tot_ind_item = orderItem.quantity
                        total = order.get_order_total()
                        tot_item = tot_ind_item
                        active_orderItem = orderItem.id
                        
                else: #if there supplement
                    #filter all order with ingredient and supplement
                    retrieve_orderItem_all= OrderItem.objects.filter(customer=customer,order = order,item = item, ingredient = choice, supplement__in = my_sup).all()
                    if retrieve_orderItem_all: # if there is one 
                        for order_item in retrieve_orderItem_all:
                            if set(order_item.supplement.all()) == set(my_sup): #check if it the same as the user request
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
                            orderItem.ingredient = choice
                            orderItem.item = item 
                            orderItem.save()
                            tot_ind_item = 1
                            total = order.get_order_total()
                    else:
                        orderItem = OrderItem.objects.create(customer = customer,order = order, quantity=1)
                        orderItem.supplement.add(*sup_id_tuple)
                        orderItem.ingredient = choice
                        orderItem.item = item 
                        orderItem.save()
                        tot_ind_item = 1
                        total = order.get_order_total()
                            
                    
                
            #ONLY ACCOMP
            if accompagment and not choice:
                print('THIS MY ACCOMP_NAME:',accompagment)
                if not supplement:  #if there is no supplement
                    #Find all order with and accompagement
                    retrieve_order_item = OrderItem.objects.filter(customer=customer,order=order,item = item,accompagnememt__in=accomp_id , ingredient= None)
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
                    retrieve_order_item = OrderItem.objects.filter(customer=customer,order=order,item = item,accompagnememt__in=accomp_id, supplement__in = sup_id ,ingredient= None)
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
                                
            
                    

            #ACCOMP + INGRE
            if accompagment and choice:
                if not supplement:     
                    retrieve_order_item = OrderItem.objects.filter(customer=customer,order=order,item = item, ingredient = choice,accompagnememt__in=accomp_id)
                    if retrieve_order_item:
                        for order_item in retrieve_order_item:
                            if (set(order_item.accompagnememt.all()) == set(my_acc) and not order_item.supplement.all()):
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
                            orderItem = OrderItem.objects.create(customer = customer,order = order, quantity =1)
                            orderItem.accompagnememt.add(*accomp_id_tuple)
                            orderItem.item = item
                            orderItem.ingredient = choice
                            orderItem.save()
                            tot_ind_item = 1
                            total = order.get_order_total()
                else: 
                    retrieve_order_item = OrderItem.objects.filter(customer=customer,order=order,item = item, ingredient = choice,accompagnememt__in=accomp_id, supplement__in = sup_id)
                    if retrieve_order_item:
                        for order_item in retrieve_order_item:
                            if ( (set(order_item.accompagnememt.all()) == set(my_acc)) and (set(order_item.supplement.all()) == set(my_sup))):
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
                            orderItem.ingredient = choice
                            orderItem.save()
                            tot_ind_item = 1
                            total = order.get_order_total()
                            
                    else:
                        print("LETS START HERE")
                        orderItem= OrderItem.objects.create(customer = customer,order = order, quantity =1)
                        orderItem.accompagnememt.add(*accomp_id_tuple)
                        orderItem.supplement.add(*sup_id_tuple)
                        orderItem.item = item
                        orderItem.ingredient = choice
                        orderItem.save()
                        tot_ind_item = 1
                        total = order.get_order_total()
                        
            # my_order_item = OrderItem.objects.filter(order= order, item = item)
            # tot_item = [sum(x.quantity for x in my_order_item)][0]
            #tot_ind_item = orderItem.quantity
            
            
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
                        'ingredient':item[i].ingredient,
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
                    #total_cart = order.get_order_quantity()
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

def CheckoutPageUpdateItem(request):



     return JsonResponse({'test':10}
                        ,safe=False)





def GetOrderCuisine(request):
    
    #Uncompleted Order
    order = Order.objects.filter(status='Sent',date_ordered__date = today).order_by('date_ordered')
    #Uncompleted Order Item
    item_selected = list()
    for ord in range(0,len(order)):
        item = order[ord].orderitem_set.all()
        for i in range(0,len(item)): 
            data = { 
                    'orderItem_id':item[i].id,
                    'order_id':item[i].order.id,
                    'order':order[ord].customer.user.first_name +" "+ order[ord].customer.user.last_name,
                    'item':item[i].item.name,
                    'quantity':item[i].quantity,
                    'ingredient':item[i].ingredient,
                    }
            item_selected.append(data)
    
    
    #Completed order
    complete_order = Order.objects.filter(complete=True,date_completed__date = today).order_by('-id')
    #Completed order item
    completed_order_item = list()
    for ord in range(0,len(complete_order)):
        item = complete_order[ord].orderitem_set.all()
        for i in range(0,len(item)): 
            data = { 
                    'order_id':item[i].order.id,
                    'order':complete_order[ord].customer.user.first_name +" "+ complete_order[ord].customer.user.last_name,
                    'item':item[i].item.name,
                    'quantity':item[i].quantity,
                    'ingredient':item[i].ingredient,
                    }
            completed_order_item.append(data)
    
    total_uncompleted_order = {
        'total_uncomplete' : order.count()
    }
    
    total_completed_order = {
        'total_complete' : complete_order.count()
    }
    
    
    return JsonResponse({"order":list(order.values()),
                         'myorder':list(item_selected),
                         'total_uncompleted_order':list(total_uncompleted_order.values()),
                         'total_completed_order':list(total_completed_order.values()),
                         'completed_order':list(complete_order.values()),
                         'completed_order_item':list(completed_order_item),})




def CuisineOptimize(request):
    
    all_order = Order.objects.filter(status='Sent',date_ordered__date = today)
    complete_order = Order.objects.filter(complete=True,date_completed__date = today).order_by('date_completed')
    
    total_completed_order = len(complete_order)
    total_uncompleted_order = len(all_order)
    
   
    
    context ={
        'all_order':all_order,
        'complete':complete_order,
         'total_completed_order':total_completed_order,
         'total_uncompleted_order':total_uncompleted_order,
    }
    
   
    return render(request,"Resto/CuisineOptimize.html",context)


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
    
        #TASK
        send_paiement_receipt.delay(order_numb)
        

    return JsonResponse("Order Completed",safe=False)



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
                'ingredient':item[i].ingredient,
                }
        item_selected.append(data)
    
    
    
    #get the data from the BackEnd
    if request.method == 'POST':
        action = request.POST['action']
        order_numb = request.POST['order']

        customer = request.user
        cust,created = Customer.objects.get_or_create(user =request.user)
        order,created = Order.objects.get_or_create(id=order_numb, customer = cust)

    
        #Process the order
        item = order.get_order_quantity()
        if item >0:
            order.status = 'Sent'
            order.transaction_id = order_number('texasgrillz')
            order.save()
            
            
        
    # order = model_to_dict(order)
    
        

    return JsonResponse({'order':10,'total_item':total_item,'orderItem':item_selected})


#Cuisine (Owner access Only)
@login_required
@permission_required('Resto.view_order',login_url='/login/') #Permission required
def Cuisine(request):
    
    #Order of the day
    #Show all order sent to the kitchen
    all_order = Order.objects.filter(status='Sent',date_ordered__date = today)
    complete_order = Order.objects.filter(complete=True,date_completed__date = today).order_by('date_completed')
    
    #Show all order sent to the kitchen yesterday
    all_order_ystd = Order.objects.filter(status='Sent',date_ordered__date = yesterday)
    complete_order_ystd = Order.objects.filter(complete=True,date_completed__date = yesterday).order_by('date_completed')
    
    
    
    #Top 5 Meals
    orderItem = OrderItem.objects.values('item__name','item__category__name').annotate(Quantity=Sum('quantity')).order_by('-Quantity')[:5]
    
    
    #viz Top 5 meals
    df = pd.DataFrame(orderItem)
    fig = px.bar(df,x='item__name', y='Quantity',color='item__category__name',text_auto='Quantity',
                 color_discrete_sequence=['bisque','crimson', 'turquoise','green','darkgreen'],opacity=0.7)
    plt = plot(fig,output_type='div')
    
    # continuous
    ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',
             'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
             'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',
             'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',
             'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',
             'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',
             'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
             'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
             'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
             'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
             'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar',
             'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
             'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid',
             'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
             'ylorrd']
    
    #descrete
    # [aliceblue, antiquewhite, aqua, aquamarine, azure,
    #         beige, bisque, black, blanchedalmond, blue,
    #         blueviolet, brown, burlywood, cadetblue,
    #         chartreuse, chocolate, coral, cornflowerblue,
    #         cornsilk, crimson, cyan, darkblue, darkcyan,
    #         darkgoldenrod, darkgray, darkgrey, darkgreen,
    #         darkkhaki, darkmagenta, darkolivegreen, darkorange,
    #         darkorchid, darkred, darksalmon, darkseagreen,
    #         darkslateblue, darkslategray, darkslategrey,
    #         darkturquoise, darkviolet, deeppink, deepskyblue,
    #         dimgray, dimgrey, dodgerblue, firebrick,
    #         floralwhite, forestgreen, fuchsia, gainsboro,
    #         ghostwhite, gold, goldenrod, gray, grey, green,
    #         greenyellow, honeydew, hotpink, indianred, indigo,
    #         ivory, khaki, lavender, lavenderblush, lawngreen,
    #         lemonchiffon, lightblue, lightcoral, lightcyan,
    #         lightgoldenrodyellow, lightgray, lightgrey,
    #         lightgreen, lightpink, lightsalmon, lightseagreen,
    #         lightskyblue, lightslategray, lightslategrey,
    #         lightsteelblue, lightyellow, lime, limegreen,
    #         linen, magenta, maroon, mediumaquamarine,
    #         mediumblue, mediumorchid, mediumpurple,
    #         mediumseagreen, mediumslateblue, mediumspringgreen,
    #         mediumturquoise, mediumvioletred, midnightblue,
    #         mintcream, mistyrose, moccasin, navajowhite, navy,
    #         oldlace, olive, olivedrab, orange, orangered,
    #         orchid, palegoldenrod, palegreen, paleturquoise,
    #         palevioletred, papayawhip, peachpuff, peru, pink,
    #         plum, powderblue, purple, red, rosybrown,
    #         royalblue, rebeccapurple, saddlebrown, salmon,
    #         sandybrown, seagreen, seashell, sienna, silver,
    #         skyblue, slateblue, slategray, slategrey, snow,
    #         springgreen, steelblue, tan, teal, thistle, tomato,
    #         turquoise, violet, wheat, white, whitesmoke,
    #         yellow, yellowgreen]
    

    # Total order of the day
    total_completed_order = complete_order.count()
    total_uncompleted_order = all_order.count()
    total_order = total_completed_order + total_uncompleted_order
    
    # Total order from the yesteray day
    total_completed_order_ystd = complete_order_ystd.count()
    total_uncompleted_order_ystd = all_order_ystd.count()
    total_order_ystd = total_completed_order + total_uncompleted_order
    
    #Total customer
    total_customer = Customer.objects.distinct().count()
    print("MY CUST",total_customer)
    
    #Order in an hour
    orderHour = Order.objects.filter(date_ordered__date = today).values('date_ordered__hour').annotate(count_order=Count('id'))
    print(orderHour)
    plt2 = "There is upcoming order"
    if orderHour:
        df2 = pd.DataFrame(orderHour)
        fig2 = px.line(df2,x='date_ordered__hour', y='count_order',markers=True,text='count_order',
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
        
    
    print("TOTAL  ORDER",total_order,total_completed_order_ystd)
    print("TOTAL COMP ORDER",total_completed_order,total_completed_order_ystd)
    
    print(complete_order_ystd)
   
   
    
    
    context = {
        'all_order':all_order,
        'complete':complete_order,
        'total_completed_order':total_completed_order,
        'total_uncompleted_order':total_uncompleted_order,
        'total_order':total_order,
        'vizTop5meals':plt,
        'vizOrder':plt2,
        'today':today,
        'visit':visit_number,
        'total_customer':total_customer,
        
    }
    return render(request,'Resto/Cuisine.html',context)



#Delete Order
def DeleteOrder(request,item_id):
    
    #Track user
    targetApp = target_app(request)

    #Get the item then delete
    del_items = OrderItem.objects.get(id = item_id)
    if request.method == 'POST':
        if request.POST.get('response') == 'Yes':
            del_items.delete()
            messages.success(request,f'{del_items} supprimé')
        elif request.POST.get('response') == 'Cancel':
            pass
        return HttpResponseRedirect(f'/texasgrillz/myorder/?session={targetApp}')
    
    context = {
          'del_item':del_items,
          'app':targetApp
    }
    return render(request, 'Resto/DeleteOrder.html',context)


def DeleteOrderItem(request):
    
    if request.method == 'POST':
        order_item_id = request.POST['item_id']
        try:
            del_items = OrderItem.objects.get(id = order_item_id)
            del_items.delete()
        except:
            del_items = SideOrderItem.objects.get(id = order_item_id)
            del_items.delete()
        
        print('DELETING',order_item_id)
    return JsonResponse('item deleted',safe=False)



#Inventory Management System
@login_required
@permission_required('Resto.view_inventory_item',login_url='/login/') #Permission required
def IventorySystem(request):
    categories = IventoryItemCategory.objects.all()
    
    if request.method == 'POST':
        form = AddProducts(request.POST)
        if form.is_valid():
            product = form.cleaned_data.get('name')
            category = form.cleaned_data.get('category')
            form.save()
            messages.success(request,f'{product} added to your inventory')
            return HttpResponseRedirect(f'/texasgrillz/inventory/')
    else:
        form = AddProducts()

    context = {
        'categorie': categories,
        'form':AddProducts
    }
    
    return render(request,'Resto/IventorySystem.html',context)


def CuisineSettings(request):
    categories = IventoryItemCategory.objects.all()
    
    if request.method == 'POST':
        
        form = AddItem(request.POST,request.FILES or None)
        form_menu = AddMenu(request.POST,request.FILES or None)
        
        if form.is_valid():
            item = form.cleaned_data.get('name')
            category = form.cleaned_data.get('category')
            #form.save()
            messages.success(request,f'{item} added to your recette list')
            return HttpResponseRedirect(f'/texasgrillz/settings/')
            
            
        elif form_menu.is_valid():
            
            menu = form_menu.cleaned_data.get('name')
            #form_menu.save()
            messages.success(request,f'{menu} added to your menu')
            print('MY MENU',menu)
            return HttpResponseRedirect(f'/texasgrillz/settings/')
    
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


def ProcessTransaction(request):
    
    if request.method == 'POST':
        user = Customer.objects.get(user = request.user)
        
        #Transaction info
        amount = request.POST.get('amount')
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
        
        
        print('working fine, just ckecking',[user,payment_method,
        amount,currency,description,operator_id,
        payment_date,status,transactionID])
        
        
        #Record Transaction
        record_trans,created = Transactions.objects.get_or_create(
        user = user,
        amount =  amount,
        currency =  currency ,
        description =  description,
        operator_id =    operator_id ,
        payment_date =  payment_date,
        status =  status ,
        transactionID = transactionID,
        payment_method =  payment_method,
        )
        
        print('END OF TRANSACTION')
        
        # #Create RDV
        # if status == 'ACCEPTED':
        #     rdv,created = rendezVous.objects.get_or_create(
        #         user = user,
        #         object = object,
        #         date = date,
        #     )
    return JsonResponse({'valider':status})

def CinetPayCredential(request):
    
    apikey = "188254710627a7eefc41627.61387840"
    site_id = "722116"
    return JsonResponse({'apiKey':apikey,'site_id':site_id})


#TASKS + JOBS
def daily_data(request):
    
    
    
    return JsonResponse({''})