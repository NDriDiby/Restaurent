
from django.shortcuts import render,redirect
from.models import Category,Item,Order,OrderItem
from django.contrib import messages
from.forms import ItemOrder
from django.contrib.auth.models import User
import json
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponseRedirect,JsonResponse
import random

# Create your views here.

def HomePage(request):
    category = Category.objects.all().order_by("name")
    context = {
        'category':category,
    }
    return render(request,'Resto/HomePage.html',context)


def MenuDetails(request,menu_id):
    menu = Category.objects.get(id = menu_id)
    category = Category.objects.all().order_by("name")
    item = Item.objects.filter(category__id = menu_id)
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = order,created= Order.objects.get_or_create(customer=customer,complete = False)
        

    else:
        item =[]
        order ={'gat_cart_total':0,'get_order_quantity':0}
        
    cartItem = order.get_order_quantity()
    print("Menu:",cartItem)

    if request.method == 'POST':
        order = ItemOrder(request.POST)
        if order.is_valid():
             item = order.cleaned_data.get('name')
             messages.success(request,f'Account Created for {item}')
             order = ItemOrder()
             return HttpResponseRedirect('/menudetails/'+menu_id+'/')

    else:
         order = ItemOrder()
    

    context = {
        'menu':menu,
        'category':category,
        'item':item,
        'orders':order,
        'cart_quantity':cartItem
    }
    return render(request,'Resto/MenuDetails.html',context)


def MyOrder(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created= Order.objects.get_or_create(customer=customer,complete = False)
        items = OrderItem.objects.filter(order = order)
        cartItem = order.get_order_quantity()
        print(cartItem)
    else:
        items =[]
        order ={'gat_cart_total':0,'get_order_quantity':0}
    
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
    order,created= Order.objects.get_or_create(customer=customer,complete = False)
    orderItem,created= OrderItem.objects.get_or_create(order = order,item = item )
  
    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity -1)

    orderItem.save()

    if orderItem.quantity <=0:
        orderItem.delete()

    return JsonResponse("Item was added",safe=False)
    


@csrf_exempt
def SendOrder(request):
    data = json.loads(request.body)
    status = data['order']
    print('status:',status)


    if status == 'sent':
        customer = request.user
        order = Order.objects.get(customer__id = customer.customer.id)
        order.status = 'sent'
        order.save()
        item = OrderItem.objects.filter(order = order)
        print(order)
        print(item)

    elif status =='completed':
        customer = request.user
        order = Order.objects.get(customer__id = customer.customer.id)
        order.status = 'completed'
        order.complete = True
        order.save()

        print('completed order')


    return JsonResponse("Order Sent",safe=False)



def Cuisine(request):
    ready=False
    all_order = Order.objects.filter(status='sent')
    complete_order = Order.objects.filter(complete=True)

    context = {
        'all_order':all_order,
        'complete':complete_order
    }
    return render(request,'Resto/Cuisine.html',context)