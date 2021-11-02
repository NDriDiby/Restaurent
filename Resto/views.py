
from django.shortcuts import render,redirect
from.models import Category,Item,Order,OrderItem
from django.contrib import messages
from.forms import ItemOrder
from django.contrib.auth.models import User
import json
from django.http.response import HttpResponseRedirect,JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
# Create your views here.

def HomePage(request):
    category = Category.objects.all().order_by("name")
    context = {
        'category':category,
    }
    return render(request,'Resto/HomePage.html',context)


@csrf_exempt
def MenuDetails(request,menu_id):
    menu = Category.objects.get(id = menu_id)
    category = Category.objects.all().order_by("name")
    item = Item.objects.filter(category__id = menu_id)
    cartItem = 10
    
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
        
        #cartItem = order.get_order_quantity
    else:
        items =[]
        order ={'gat_cart_total':0,'get_order_quantity':0}
    
    context = {
        'order':order,
        'items':items,
       # 'cart_quantity':cartItem

    }    
    return render(request,'Resto/MyOrder.html',context)



def UpdatedItem(request):
    data = json.loads(request.body)
    itemId = data['itemId']
    action = data['action']

    print('ItemId:',itemId)
    print('action:',action)

    def generate_random_number():
        for i in range(0,4):
            numb = random.randint(0,10)
        return numb


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

    return JsonResponse("Item was added",safe = False)
    

