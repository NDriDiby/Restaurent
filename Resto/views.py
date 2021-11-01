from django.shortcuts import render,redirect
from.models import Category,Item,Order,OrderItem
from django.contrib import messages
from.forms import ItemOrder
from django.http.response import HttpResponseRedirect,JsonResponse
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
        'orders':order
    }
    return render(request,'Resto/MenuDetails.html',context)


def MyOrder(request):
    order = Order.objects.get(id =1)
    items = OrderItem.objects.filter(order__transaction_id = 1)
   
    context = {
        'order':order,
        'items':items,

    }    
    return render(request,'Resto/MyOrder.html',context)
