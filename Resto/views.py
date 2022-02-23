import re
from django.shortcuts import render,redirect
from django.test import ignore_warnings
from.models import (Category,Customer,Item,Order,OrderItem,ItemChoices,
                    IventoryItem,IventoryItemCategory)
from django.contrib import messages
from.forms import CustomerForm,ItemChoiceForm,AddProducts
from django.contrib.auth.models import User
import json
from Customer.utils import track_session,order_number,get_table_number,target_app
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http.response import HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import permission_required,login_required
import random
from datetime import datetime,timedelta,time
from django.utils import timezone
from Bakerys.forms import OrderForm
from django.db.models import F
from django.db.models import Max,Sum
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
 

 #App Name
app = Order._meta.app_label

today = timezone.localtime(timezone.now()).date()



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
        cust.phone = request.GET.get('phone')
        cust.save()
        
        print("THIS MY PHONE NUMBER",cust.phone)
        
        
    
        #Show order to customer
        order_sent = Order.objects.filter(customer = cust, status = 'Sent', table =table, date_ordered__date = today).last()
        
        

    context = {
        'category':category,
        'order':order_sent,
        'app':targetApp
    }
    return render(request,'Resto/HomePage.html',context)


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
    
    
    #Create customer and order
    
    # Authenticate then create an order
    if request.user.is_authenticated:
        try:
            username = User.objects.get(id=request.user.id)
            cust,created = Customer.objects.get_or_create(user =request.user)
            order,created= Order.objects.get_or_create(customer=cust,status='Pending',table=table)
            cartItem = order.get_order_quantity()
            
        except:
            pass
            
    
    context = {
        'menu':menu,
        'category':category,
        'item':item,
        'orders':order,
        'cart_quantity':cartItem,
        'app':targetApp
        
    }
    return render(request,'Resto/MenuDetails.html',context)


def ItemDetails(request,item_id):
    
    #Item
    order = None
    cartItem = 0

    #Form
    form = ItemChoiceForm()
    form.base_fields['name'].queryset = ItemChoices.objects.filter(parent_food_id = item_id,choice_category__name__icontains= 'Assaisonement')
    
    #Choice Category
    assaisonement = ItemChoices.objects.filter(parent_food_id= item_id, choice_category__name__icontains= 'Assaisonnement')
    cuisson = ItemChoices.objects.filter(parent_food_id= item_id, choice_category__name__icontains= 'Cui')
    ingredients = ItemChoices.objects.filter(parent_food_id= item_id, choice_category__name__icontains= 'ingredients')
    eau_mineral = ItemChoices.objects.filter(parent_food_id= item_id, choice_category__name__icontains= 'eau mineral')
    coca_cola_produit = ItemChoices.objects.filter(parent_food_id= item_id, choice_category__name__icontains= 'coca-cola')
    
    
    #Get Table Number
    table = get_table_number(request)
    
    #Track user
    targetApp = target_app(request)
    
    
    item = Item.objects.get(id=item_id)
    cartItem = 0
    myItem = None
    
    if request.user.is_authenticated:
        try:
            #Retrive the order
            cust,created = Customer.objects.get_or_create(user =request.user)
            order,created= Order.objects.get_or_create(customer=cust,status='Pending',table=table)
            cartItem = order.get_order_quantity()
            
            
    
            #Check for past or pending order for the user
            pending_order = Order.objects.filter(customer=cust,status='Pending')
            if len(pending_order) > 1:
                print(pending_order)
                pending_order.delete()
                messages.warning(request,"Vous ne pouvez pas passer de commande sur plusieurs tables")
                messages.success(request,f"Votre nouveau numéro de table est {table}")
                order,created= Order.objects.get_or_create(customer=cust,status='Pending',table=table)
                return HttpResponseRedirect(f'/texasgrillz/?session={targetApp}')
                
                
            
            if request.method == 'POST':
                order_table = request.POST.get('item')
                order_item_id = request.POST.get('orderItemId')
                ingre = request.POST.get('ingredient')
                saiss = request.POST.get('assaisonement')
                cuiss = request.POST.get('cuisson')
                choice = ingre,saiss,cuiss
                
            
                
              
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
        'myitem':myItem
        
    }
    
    return render (request,'Resto/ItemsDetails.html',context)
    


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
        
        
    if request.method == 'POST':
        #redirect to HomePage
        order_id= request.POST.get("order")
        order= Order.objects.get(id = order_id)
        items = order.orderitem_set.all()
        cartItem = order.get_order_quantity()
        if cartItem > 0:
            messages.success(request,f"{order.customer.user.first_name}, votre commande a été bien réçu par notre cuisine!")
        else:
            messages.warning(request,"Votre panier est vide")
            
        return HttpResponseRedirect(f'/texasgrillz/?session={targetApp}')

   
        
    context = {
        'order':order,
        'items':items,
        'cart_quantity':cartItem,
        'app':targetApp
    }    
    return render(request,'Resto/MyOrder.html',context)


#Backend Process of Item
def UpdatedItem(request):
    
    
    #Get the response from the backend
    data = json.loads(request.body)
    itemId = data['itemId']
    action = data['action']
    choice = data['choice']
    
    

    #Update the Cart of the current user
    customer,created= Customer.objects.get_or_create(user = request.user)
    item = Item.objects.get(id=itemId)
    order,created= Order.objects.get_or_create(customer=customer,status = 'Pending')
    orderItem,created= OrderItem.objects.get_or_create(order = order,item = item, ingredient = choice)
    
    
    
    
    #Increase item
    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
        orderItem.save()

    #Decrease item
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        orderItem.save()

    #Delete item
    if orderItem.quantity<=0:
        orderItem.delete()

    return JsonResponse(f'Item was {action}',safe=False)
    


#BackEnd process of Order
def SendOrder(request):

    #get the data from the BackEnd
    data = json.loads(request.body)
    action = data['action']
    order_numb = data['order']
    
    customer = request.user
    
    

    
    #Process the order
    if request.method == 'POST' and action == 'sent':
        
        order = Order.objects.filter(customer__id = customer.customer.id).last()
        item = order.get_order_quantity()
        if item >0:
            order.status = 'Sent'
            order.transaction_id = order_number('texasgrillz')
            order.save()
        #     messages.success(request,f"{order.customer.user.first_name}, votre commande a été bien réçu par notre cuisine!")
        # else:
        #     messages.warning(request,"Votre panier est vide")

    
    elif action =='completed':
        order = Order.objects.get(id = order_numb)
        order.status = 'Completed'
        order.complete = True
        order.date_completed = timezone.localtime()
        order.save()
        
        
        subject = f"Commande: {order.transaction_id}"
        newline = "\n"
        message = f"Salut {order.customer.user.first_name},{newline}{newline}Votre commande est prete. Vous recevrez votre commande sous peu ci-dessous est votre reçu de commande.{newline}\
            {newline}Order Number: {order.transaction_id} \
            {newline}Order Total: {order.get_order_total()} FCFA\
            {newline}"
            
        send_mail(subject,message,
                          settings.EMAIL_HOST_USER,
                          [order.customer.user.email],fail_silently=False,)
        

    return JsonResponse("Order Sent",safe=False)


#Cuisine (Owner access Only)
@login_required
@permission_required('Resto.view_order',login_url='/login/') #Permission required
def Cuisine(request):
    
    
   
    #Order of the day
    #Show all order sent to the kitchen
    all_order = Order.objects.filter(status='Sent',date_ordered__date = today)
    complete_order = Order.objects.filter(complete=True,date_completed__date = today).order_by('date_completed')
    
    # order_item = OrderItem.objects.all()
    # top_item_number = order_item.aggregate(Sum('quantity'))
    # top_item_number = top_item_number['quantity__sum']
    # top_item =order_item.get(quantity = top_item_number)
    
    
    # print("MOST ORDERED",top_item)
    # print('TOP ITEM',top_item_number)

    # Total order of the day
    total_completed_order = len(complete_order)
    total_uncompleted_order = len(all_order)
    
    context = {
        'all_order':all_order,
        'complete':complete_order,
        'total_completed_order':total_completed_order,
        'total_uncompleted_order':total_uncompleted_order,
        # 'top_item':top_item,
        # 'top_item_number':top_item_number,
        'today':today
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




