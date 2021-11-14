
from django.shortcuts import render,redirect
from.models import Category,Customer,Item,Order,OrderItem
from django.contrib import messages
from.forms import CustomerForm
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http.response import HttpResponseRedirect,JsonResponse
from django.contrib.auth.decorators import permission_required,login_required
import random
import datetime
 

 #App Name
app = Order._meta.app_label



# Create your views here.
def HomePage(request):
    order = None
    print('myAppName:',Order._meta.app_label)
    request.session[str(app)] = app
    print(str(app))

    category = Category.objects.all().order_by("name")
    if request.user.is_authenticated:
        customer = request.user
        order= Order.objects.filter(customer__name = customer, status = 'Sent').last()
        
    else:
        category = Category.objects.all().order_by("name")

    context = {
        'category':category,
        'order':order
    }
    return render(request,'Resto/HomePage.html',context)


def MenuDetails(request,menu_id):
    menu = Category.objects.get(id = menu_id)
    category = Category.objects.all().order_by("name")
    item = Item.objects.filter(category__id = menu_id)
    all_user = User.objects.values_list('username',flat=True)

    if request.session.has_key(str(app)):
        print(app)
    

    
    if request.user.is_authenticated:
        username = User.objects.get(id=request.user.id)
        cust,created = Customer.objects.get_or_create(user =request.user)
        cust.name = username.username
        cust.save()
        customer = request.user.customer
        order,created= Order.objects.get_or_create(customer=customer,status='Pending')
        cartItem = order.get_order_quantity()

    else:
        return HttpResponseRedirect('/register/')

        
    if request.method == 'POST':
        order_table = request.POST.get('item')
        order_table = Item.objects.filter(id=order_table)
        order_table = order_table[0]
        messages.success(request,f'{order_table} added to your table')
    
    
    context = {
        'menu':menu,
        'category':category,
        'item':item,
         'orders':order,
        'cart_quantity':cartItem,
    }
    return render(request,'Resto/MenuDetails.html',context)


def MyOrder(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created= Order.objects.get_or_create(customer=customer,status='Pending')
        items = order.orderitem_set.all()
        cartItem = order.get_order_quantity()

    if request.method == 'POST':
        
        return redirect('homepage-texasgrillz')

    context = {
        'order':order,
        'items':items,
        'cart_quantity':cartItem
    }    
    return render(request,'Resto/MyOrder.html',context)



def UpdatedItem(request):
    data = json.loads(request.body)
    itemId = data['itemId']
    action = data['action']

    print('ItemId:',itemId)
    print('action:',action)

    customer = request.user.customer
    item = Item.objects.get(id=itemId)
    order= Order.objects.get(customer=customer,status = 'Pending')
    orderItem,created= OrderItem.objects.get_or_create(order = order,item = item )
  
    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
        orderItem.save()

    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
        orderItem.save()

    if orderItem.quantity<=0:
        orderItem.delete()

    return JsonResponse(f'Item was {action}',safe=False)
    


@csrf_protect
def SendOrder(request):
    data = json.loads(request.body)
    action = data['action']
    order_numb = data['order']
    print('status:',action)
    print('order_number:',order_numb)

    if request.method == 'POST' and action == 'sent':
        customer = request.user
        order = Order.objects.filter(customer__id = customer.customer.id).last()
        item = order.get_order_quantity()
        print('order quant:',item)
        if item >0:
            order.status = 'Sent'
            order.save()
            messages.success(request,"Order Sent to kitchen")
            print('order saved')

        else:
            print("I can't send your order")
            messages.warning(request,"Your cart is empty")

    
    elif action =='completed':
        order = Order.objects.get(id = order_numb)
        order.status = 'Completed'
        order.complete = True
        order.save()
        print('completed order')

    order.save()
    

    return JsonResponse("Order Sent",safe=False)


@csrf_protect
@login_required
@permission_required('Resto.view_order',login_url='/login/')
def Cuisine(request):

    all_order = Order.objects.filter(status='Sent')
    complete_order = Order.objects.filter(complete=True)
    
    context = {
        'all_order':all_order,
        'complete':complete_order
    }
    return render(request,'Resto/Cuisine.html',context)



def ProcessOrder(request):


    return JsonResponse("your order",safe=False)



def DeleteOrder(request,item_id):

    del_items = OrderItem.objects.get(id = item_id)
    print(del_items)
    if request.method == 'POST':
        if request.POST.get('response') == 'Yes':
            del_items.delete()
        elif request.POST.get('response') == 'Cancel':
            pass
        return HttpResponseRedirect('/myorder')
    
    context = {
          'del_item':del_items
    }
    return render(request, 'Resto/DeleteOrder.html',context)