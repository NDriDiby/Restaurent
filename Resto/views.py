
from django.shortcuts import render,redirect
from.models import Category,Customer,Item,Order,OrderItem
from django.contrib import messages
from.forms import CustomerForm
from django.contrib.auth.models import User
import json
from Customer.utils import track_session,order_number,get_table_number,target_app
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http.response import HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import permission_required,login_required
import random
import datetime
from Bakerys.forms import OrderForm
 

 #App Name
app = Order._meta.app_label



#HomePage
def HomePage(request):
    
    #Table Number
    table = get_table_number(request)
    if table == None:
        pass
    
    #Track user
    session = track_session(request)
    targetApp = target_app(request) #session=bakerys/?table=x
    
    
    order = None #set order to none
    category = Category.objects.all().order_by("name") #Order the category by name

    
    if request.user.is_authenticated:

        
        #Create a customer object
        cust,created = Customer.objects.get_or_create(user =request.user)
        username = User.objects.get(id=request.user.id)
        cust.name = username.username
        cust.save()
        
        #Create Order
        order,created= Order.objects.get_or_create(customer=cust,status='Pending',
        table=table)
        print('Table Number:',order.table)
        
        
        #Show order to customer
        order_sent = Order.objects.filter(customer = cust, status = 'Sent').last()

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
    cartItem = None
    
    
    #Create customer and order
    # Authenticate then create an order
    if request.user.is_authenticated:
        try:
            username = User.objects.get(id=request.user.id)
            cust,created = Customer.objects.get_or_create(user =request.user)
            cust.name = username.username
            cust.save()
            order,created= Order.objects.get_or_create(customer=cust,status='Pending')
            cartItem = order.get_order_quantity()
            print("Found the order")
        except:
            messages.warning(request,"Can't pass order on multiple table")
            messages.success(request,f"Your new table number is {table}")
            pending_order = Order.objects.filter(customer=cust,status='Pending')
            pending_order[0].delete()
            order,created= Order.objects.get_or_create(customer=cust,status='Pending',table=table)
            cartItem = order.get_order_quantity()
            return HttpResponseRedirect(f'/texasgrillz?session={targetApp}')
            

    # Create new account
    else:
        return HttpResponseRedirect(f'/register?session={targetApp}')

    
    # Show item added to cart
    if request.method == 'POST':
        order_table = request.POST.get('item')
        order_table = Item.objects.filter(id=order_table)
        order_table = order_table[0]
        messages.success(request,f'{order_table} ajouté a votre table')
    
    
    context = {
        'menu':menu,
        'category':category,
        'item':item,
         'orders':order,
        'cart_quantity':cartItem,
        'app':targetApp
        
    }
    return render(request,'Resto/MenuDetails.html',context)


#My Order
def MyOrder(request):
    
    #Grab the Table number from the url using request
    table = get_table_number(request)

    #Track user
    targetApp = target_app(request)

    #get the Order and  items
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created= Order.objects.get_or_create(customer=customer,status='Pending',table=table)
        items = order.orderitem_set.all()
        cartItem = order.get_order_quantity()

    if request.method == 'POST':
        #redirect to HomePage
        return HttpResponseRedirect(f'/texasgrillz?session={targetApp}')

   
        
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

    #Update the Cart of the current user
    customer, created= Customer.objects.get_or_create(user = request.user)
    item = Item.objects.get(id=itemId)
    order= Order.objects.get(customer=customer,status = 'Pending')
    orderItem,created= OrderItem.objects.get_or_create(order = order,item = item )
  
    #Increase quantity
    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
        orderItem.save()

    #Decrese quantity
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        orderItem.save()

    #Delete item
    if orderItem.quantity<=0:
        orderItem.delete()

    return JsonResponse(f'Item was {action}',safe=False)
    


#BackEnd process of Order
@csrf_protect
def SendOrder(request):

    #get the data from the BackEnd
    data = json.loads(request.body)
    action = data['action']
    order_numb = data['order']
    cust_note = data['note']
    print('status:',action)
    print('order_number:',order_numb)
    print('cust_note:',cust_note)
    customer = request.user
    #Process the order
    if request.method == 'POST' and action == 'sent':
        
        order = Order.objects.filter(customer__id = customer.customer.id).last()
        item = order.get_order_quantity()
        if item >0:
            order.status = 'Sent'
            order.transaction_id = order_number('texasgrillz')
            order.note = cust_note
            order.save()
            messages.success(request,f"{customer}, votre commande a été bien reću par notre cuisine!")
        else:
            messages.warning(request,"Your cart is empty")

    
    elif action =='completed':
        order = Order.objects.get(id = order_numb)
        order.status = 'Completed'
        order.complete = True
        order.save()
        messages.success(request,f"{customer}, your order is completed")

    order.save()
    
    return JsonResponse("Order Sent",safe=False)


#Cuisine (Owner access Only)
@csrf_protect
@login_required
@permission_required('Resto.view_order',login_url='/login/') #Permission required
def Cuisine(request):

    #Show all order sent to the kitchen
    all_order = Order.objects.filter(status='Sent')
    complete_order = Order.objects.filter(complete=True)
    
    context = {
        'all_order':all_order,
        'complete':complete_order
    }
    return render(request,'Resto/Cuisine.html',context)



def ProcessOrder(request):


    return JsonResponse("your order",safe=False)



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