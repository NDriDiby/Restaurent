from cProfile import label
from cgitb import text
from itertools import count
from multiprocessing import context
import re
from django.db import reset_queries
from django.shortcuts import render,redirect
from django.test import ignore_warnings
from.models import (Accompagnement, Category,Customer,Item,Order,OrderItem,ItemChoices,
                    IventoryItem,IventoryItemCategory)
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
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
from django.core import serializers
from django.forms.models import model_to_dict
from plotly.offline import plot
import plotly.express as px
import pandas as pd
import calendar


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
        'app':targetApp
    }
    return render(request,'Resto/HomePageNew.html',context)


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
            
            print('My next order',order.date_ordered)
            current_time = timezone.localtime(timezone.now())
            if (order.date_ordered < current_time):
                time_diff = (current_time - order.date_ordered)
                print('it is been',round(time_diff.seconds/60))
                if ((time_diff.seconds/60) >= 10):
                    order.delete()
                    print("ORDER DELETED")
            
        except:
            pass
        
        
    
    context = {
        'menu':menu,
        'category':category,
        'item':item,
        'orders':order,
        'cart_quantity':cartItem,
        'cart_total':cartTotal,
        'app':targetApp
        
    }
    return render(request,'Resto/MenuDetailsNew.html',context)


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
    assaisonement = ItemChoices.objects.filter(parent_food_id= item_id, choice_category__name__icontains= 'Assaisonne')
    cuisson = ItemChoices.objects.filter(parent_food_id= item_id, choice_category__name__icontains= 'Cui')
    ingredients = ItemChoices.objects.filter(parent_food_id= item_id, choice_category__name__icontains= 'ingredients')
    eau_mineral = ItemChoices.objects.filter(parent_food_id= item_id, choice_category__name__icontains= 'eau mineral')
    coca_cola_produit = ItemChoices.objects.filter(parent_food_id= item_id, choice_category__name__icontains= 'coca-cola')
    
    print('it is assaisonment',assaisonement)
    #Get Table Number
    table = get_table_number(request)
    
    #Track user
    targetApp = target_app(request)
    
    
    item = Item.objects.get(id=item_id)
    print('THIS IS MY ITEM-ACCOMP',item.accompagnement.all())
    cartItem = 0
    myItem = None
    my_total = 0
    
    if request.user.is_authenticated:
        try:
            #Retrive the order
            cust,created = Customer.objects.get_or_create(user =request.user)
            order,created= Order.objects.get_or_create(customer=cust,status='Pending',table=table)
            cartItem = order.get_order_quantity()
            my_total = order.get_order_total()
            
            #Check for past or pending order for the user
            pending_order = Order.objects.filter(customer=cust,status='Pending')
            if len(pending_order) > 1:
                pending_order.delete()
                messages.warning(request,"Vous ne pouvez pas passer de commande sur plusieurs tables")
                messages.success(request,f"Votre nouveau numéro de table est {table}")
                order,created= Order.objects.get_or_create(customer=cust,status='Pending',table=table)
                return HttpResponseRedirect(f'/texasgrillz/?session={targetApp}')
                
                
            
            if request.method == 'POST':
                order_table = request.POST.get('item')
                
                
                myitem = Item.objects.get(id=order_table)
                my_order_item = OrderItem.objects.filter(order= order, item = myitem)
                tot_item = [sum(x.quantity for x in my_order_item)][0]
                messages.success(request,f"({tot_item}) {myitem} ajouté votre table")
                
                
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
        

        
    context = {
        'order':order,
        'items':items,
        'cart_quantity':cartItem,
        'app':targetApp
    }    
    return render(request,'Resto/MyOrder.html',context)


#Backend Process of Item
def UpdatedItem(request):
    
    customer = request.user
    order = Order.objects.filter(customer__id = customer.customer.id).last()
 
    
    item_name = None
    total_cart = None
    tot_item= None
    total_accomp = 0
    
    
    if request.method == 'POST':
        
        itemId = request.POST['itemId']
        action = request.POST['action']
        choice = request.POST.get('choice')
        accompagment = request.POST.get('accomp')
        
        #Update the Cart of the current user
        customer,created= Customer.objects.get_or_create(user = request.user)
        item = Item.objects.get(id=itemId)
        #accomp = Accompagnement.objects.filter(id=int(accompagment))
        #print('ADD THIS TO MY ORDER',accomp)
        order,created= Order.objects.get_or_create(customer=customer,status = 'Pending')
        orderItem,created= OrderItem.objects.get_or_create(order = order,item = item, ingredient = choice)
        item_name = item.name
        
        
        #Increase item
        if action =='add':
            orderItem.quantity = (orderItem.quantity + 1)
            orderItem.save()
            
            
        #Decrease item
        elif action == 'remove':
            orderItem.quantity = (orderItem.quantity - 1)
            orderItem.save()

        #Delete item
        elif orderItem.quantity<=0:
             orderItem.delete()
            
            
        my_order_item = OrderItem.objects.filter(order= order, item = item)
        tot_item = [sum(x.quantity for x in my_order_item)][0]
        tot_ind_item = orderItem.quantity
        total_cart = order.get_order_quantity()
        if accompagment:
            accompagment = [int(x) for x in accompagment.split(',')]
            print('MY ACCOM_ID', accompagment)
            accomp = Accompagnement.objects.filter(id__in=accompagment)
            print('ADD THIS TO MY ORDER',accomp)
            total_accomp = sum([acc.prix for acc in accomp])
            print('ORDER ACCOMP TOT',total_accomp)
            total = order.get_order_total() + total_accomp
        else:
            total = order.get_order_total()
             
        print("MY TOTAL",total)

        active_orderItem = orderItem.id
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
                    'total':item[i].get_total(),
                    'item_price':item[i].item.prix,
                    }
            item_selected.append(data)
            
        


    return JsonResponse({"item_name":item_name,
                         'total_cart':total_cart,
                         'tot_item':tot_item,
                         'tot_ind_item':tot_ind_item,
                         'total':total,
                         'orderItem':item_selected,
                         'active_orderItem':active_orderItem,
                         'total_accomp':total_accomp,
                         },safe=False)



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
        
        # subject = f"Commande: {order.transaction_id}"
        # newline = "\n"
        # message = f"Salut {order.customer.user.first_name},{newline}{newline}Votre commande est prete. Vous recevrez votre commande sous peu ci-dessous est votre reçu de commande.{newline}\
        #         {newline}Order Number: {order.transaction_id} \
        #         {newline}Order Total: {order.get_order_total()} FCFA\
        #         {newline}"
            
        # send_mail(subject,message,
        #                   settings.EMAIL_HOST_USER,
        #                   [order.customer.user.email],fail_silently=False,)
        
        

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
        
    #     subject = f"Commande: {order.transaction_id}"
    #     newline = "\n"
    #     message = f"Salut {order.customer.user.first_name},{newline}{newline}Votre commande est prete. Vous recevrez votre commande sous peu ci-dessous est votre reçu de commande.{newline}\
    #         {newline}Order Number: {order.transaction_id} \
    #         {newline}Order Total: {order.get_order_total()} FCFA\
    #         {newline}"
            
    #     send_mail(subject,message,
    #                       settings.EMAIL_HOST_USER,
    #                       [order.customer.user.email],fail_silently=False,)
    order = model_to_dict(order)
    
        

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


