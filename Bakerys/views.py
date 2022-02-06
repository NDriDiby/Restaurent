from django.shortcuts import render,redirect
from Resto.models import Customer
from .models import CategoryBakerys,OrderBakerys,ItemBakerys,OrderItemBakerys,CustomerBakerys
import json
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http.response import HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import permission_required,login_required
from django.apps import AppConfig
from django.conf import settings
from Customer.utils import track_session,order_number,get_table_number,target_app
from django.urls import resolve,ResolverMatch
from.forms import OrderForm




#www.Icarus.com/bakerys?session=bakerys&table=X



#Home Page
def HomePageBakerys(request):

    #Table Number
    table = get_table_number(request)
    if table == None:
        pass
    
    #Track user
    session = track_session(request)
    targetApp = target_app(request) #session=bakerys/?table=x
    
    #Category to choose from
    order_sent = None
    category = CategoryBakerys.objects.all().order_by("name")

    
    if request.user.is_authenticated:
       
        #Create a customer object
        cust,created = CustomerBakerys.objects.get_or_create(user =request.user)
        username = User.objects.get(id=request.user.id)
        cust.name = username.username
        cust.save()

        #Create Order
        order,created= OrderBakerys.objects.get_or_create(customer=cust,status='Pending',
        table=table)
        print('Table Number:',order.table)

        #Show order to customer
        order_sent = OrderBakerys.objects.filter(customer = cust, status = 'Sent').last()
        
    

    context = {
        'category':category,
        'order':order_sent,
        'session':session,
         'app':targetApp
    }
    return render(request,'Bakerys/HomePage.html',context)


# Menu Details 
def MenuDetailsBakerys(request,menu_id):

    #Get Table Number
    table = get_table_number(request)

    #Track user
    targetApp = target_app(request)

    #Get and show the item in each category
    menu = CategoryBakerys.objects.get(id = menu_id)
    category = CategoryBakerys.objects.all().order_by("name")
    item = ItemBakerys.objects.filter(category__id = menu_id)
    
    
    order = None
    cartItem = None

    # Authenticate then create an order
    if request.user.is_authenticated:
        try:
            username = User.objects.get(id=request.user.id)
            cust,created = CustomerBakerys.objects.get_or_create(user =request.user)
            cust.name = username.username
            cust.save()
            order,created= OrderBakerys.objects.get_or_create(customer=cust,status='Pending')
            cartItem = order.get_order_quantity()
        except:
            messages.warning(request,"Can't pass order on multiple table")
            messages.success(request,f"Your new table number is {table}")
            pending_order = OrderBakerys.objects.filter(customer=cust,status='Pending')
            pending_order[0].delete()
            order,created= OrderBakerys.objects.get_or_create(customer=cust,status='Pending',table=table)
            cartItem = order.get_order_quantity()
            return HttpResponseRedirect(f'/bakerys?session={targetApp}')
            

    # Create new account
    else:
        return HttpResponseRedirect(f'/register?session={targetApp}')

    
    # Show item added to cart
    if request.method == 'POST':
        order_table = request.POST.get('item')
        order_table = ItemBakerys.objects.filter(id=order_table)
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
    return render(request,'Bakerys/MenuDetails.html',context)


# Customer Order
def MyOrderBakerys(request):

    #Grab the Table number from the url using request
    table = get_table_number(request)

    #Track user
    targetApp = target_app(request)
    

    #Get Order
    if request.user.is_authenticated:
        cust,created = CustomerBakerys.objects.get_or_create(user =request.user)
        order,created= OrderBakerys.objects.get_or_create(customer=cust,status='Pending',table=table)
        items = order.orderitembakerys_set.all()
        cartItem = order.get_order_quantity()

    #Form Validation
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect(f'/bakerys?session={targetApp}')

    else:
        form = OrderForm()


    context = {
        'order':order,
        'items':items,
        'cart_quantity':cartItem,
        'form':form,
        'app':targetApp
        }    

    return render(request,'Bakerys/MyOrder.html',context)


#Increase and Decrease cart item
def UpdatedItemBakerys(request):
    data = json.loads(request.body)
    itemId = data['itemId']
    action = data['action']

    print('ItemId:',itemId)
    print('action:',action)

    #Retrive the order
    cust,created = CustomerBakerys.objects.get_or_create(user =request.user)
    item = ItemBakerys.objects.get(id=itemId)
    order= OrderBakerys.objects.get(customer=cust,status = 'Pending')
    orderItem,created= OrderItemBakerys.objects.get_or_create(order = order,item = item )
  
    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
        orderItem.save()

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        orderItem.save()

    if orderItem.quantity<=0:
        orderItem.delete()

    return JsonResponse(f'Item {action}',safe=False)
    


#Send order to the Kitchen
@csrf_protect
def SendOrderBakerys(request):
    data = json.loads(request.body)
    action = data['action']
    order_numb = data['order']
    cust_note = data['note']
    print('status:',action)
    print('order_number:',order_numb)
    print('cust_note:',cust_note)


    if request.method == 'POST' and action == 'sent':
        #Retrieve the order then send to the kitchen
        customer = request.user
        cust,created = CustomerBakerys.objects.get_or_create(user =request.user)
        order,created = OrderBakerys.objects.get_or_create(id=order_numb, customer = cust)
        item = order.get_order_quantity()
        if item >0:
            order.status = 'Sent'
            order.transaction_id = order_number('bakerys')
            order.note = cust_note
            order.save()
            messages.success(request,f"{customer}, votre commande a été bien réçu par notre cuisine!")

        else:
            messages.warning(request,"Your cart is empty")

    #Order Completed
    elif action =='completed':
        order = OrderBakerys.objects.get(id = order_numb)
        order.status = 'Completed'
        order.complete = True
        order.save()
        messages.success(request,"Order is completed")


    return JsonResponse("Order Sent",safe=False)


#Delete Order
def DeleteOrderBakerys(request,item_id):

    #Track user
    targetApp = target_app(request)
             
    del_items = OrderItemBakerys.objects.get(id = item_id)
    print(del_items)
    if request.method == 'POST':
        if request.POST.get('response') == 'Yes':
            del_items.delete()
            messages.success(request,f'{del_items} supprimé')
        elif request.POST.get('response') == 'Cancel':
            pass
        return HttpResponseRedirect(f'/bakerys/myorder/?session={targetApp}')
    
    context = {
          'del_item':del_items,
          'app':targetApp
    }
    return render(request, 'Bakerys/DeleteOrder.html',context)


#Cuisine Access
@csrf_protect
@login_required
@permission_required('Resto.view_order',login_url='/login/')
def CuisineBakerys(request):

    all_order = OrderBakerys.objects.filter(status='Sent')
    complete_order = OrderBakerys.objects.filter(complete=True)
    
    context = {
        'all_order':all_order,
        'complete':complete_order
    }
    return render(request,'Bakerys/Cuisine.html',context)