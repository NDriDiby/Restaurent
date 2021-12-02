from django.shortcuts import render,redirect
from Resto.models import Customer
from .models import Category,OrderBakerys,ItemBakerys,OrderItemBakerys,CustomerBekerys
import json
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http.response import HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import permission_required,login_required
from django.apps import AppConfig
from django.conf import settings
from Customer.utils import track_session
from django.urls import resolve,ResolverMatch
from.forms import OrderForm


#www.Icarus.com/bakerys?session=bakerys/?table=X

#App Name
app = OrderBakerys._meta.app_label+"?table=14"

#Home Page
def HomePageBakerys(request):
    #Grab the Table number from the url using request
    table = request.GET.get('table')
    if table is None:
        table = 1
    else:
        table = int(table[:-1])
    print(type(table))
    print('Table Number:',table)

    #Track user
    session = track_session(request)
    
    #Category to choose from
    order_sent = None
    category = Category.objects.all().order_by("name")

    
    if request.user.is_authenticated:
        #Create a customer object and an order
        cust,created = CustomerBekerys.objects.get_or_create(user =request.user)
        username = User.objects.get(id=request.user.id)
        cust.name = username.username
        cust.save()
        order,created= OrderBakerys.objects.get_or_create(customer=cust,status='Pending',table=table)

        #Show order to customer
        order_sent = OrderBakerys.objects.filter(customer = cust, status = 'Sent').last()
        
    else:
        category = Category.objects.all().order_by("name")

    context = {
        'category':category,
        'order':order_sent,
        'session':session,
    }
    return render(request,'Bakerys/HomePage.html',context)


# Menu Details 
def MenuDetailsBakerys(request,menu_id):
    menu = Category.objects.get(id = menu_id)
    category = Category.objects.all().order_by("name")
    item = ItemBakerys.objects.filter(category__id = menu_id)
    
    # Authenticate then create an order
    if request.user.is_authenticated:
        username = User.objects.get(id=request.user.id)
        cust,created = CustomerBekerys.objects.get_or_create(user =request.user)
        cust.name = username.username
        cust.save()
        order,created= OrderBakerys.objects.get_or_create(customer=cust,status='Pending')
        cartItem = order.get_order_quantity()
    
    # Create new account
    else:
        return HttpResponseRedirect(f'/register?session={app}')

    
    # Show item added to cart
    if request.method == 'POST':
        order_table = request.POST.get('item')
        order_table = ItemBakerys.objects.filter(id=order_table)
        order_table = order_table[0]
        messages.success(request,f'{order_table} added to your table')
    
    
    context = {
        'menu':menu,
        'category':category,
        'item':item,
         'orders':order,
        'cart_quantity':cartItem,
        
    }
    return render(request,'Bakerys/MenuDetails.html',context)


# Customer Order
def MyOrderBakerys(request):

    #Get Order
    if request.user.is_authenticated:
        cust,created = CustomerBekerys.objects.get_or_create(user =request.user)
        order,created= OrderBakerys.objects.get_or_create(customer=cust,status='Pending')
        items = order.orderitembakerys_set.all()
        cartItem = order.get_order_quantity()

    #Form Validation
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            #form.save()
            return HttpResponseRedirect(f'/bakerys?session={app}')

    else:
        form = OrderForm()


    context = {
        'order':order,
        'items':items,
        'cart_quantity':cartItem,
        'form':form}    

    return render(request,'Bakerys/MyOrder.html',context)


#Increase and Decrease cart item
def UpdatedItemBakerys(request):
    data = json.loads(request.body)
    itemId = data['itemId']
    action = data['action']

    print('ItemId:',itemId)
    print('action:',action)

    #Retrive the order
    cust,created = CustomerBekerys.objects.get_or_create(user =request.user)
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
        cust,created = CustomerBekerys.objects.get_or_create(user =request.user)
        order,created = OrderBakerys.objects.get_or_create(id=order_numb, customer = cust)
        item = order.get_order_quantity()
        if item >0:
            order.status = 'Sent'
            order.note = cust_note
            order.save()
            messages.success(request,"Order Sent to kitchen")


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
             
    del_items = OrderItemBakerys.objects.get(id = item_id)
    print(del_items)
    if request.method == 'POST':
        if request.POST.get('response') == 'Yes':
            del_items.delete()
        elif request.POST.get('response') == 'Cancel':
            pass
        return redirect('order-bakerys')
    
    context = {
          'del_item':del_items
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