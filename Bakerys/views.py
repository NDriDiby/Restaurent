from django.shortcuts import render
from Resto.models import Order,Item,OrderItem,Customer
from .models import Category
from django.http.response import HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages




# Create your views here.
def HomePage(request):
    order = None
    category = Category.objects.all().order_by("name")
    if request.user.is_authenticated:
        customer = request.user
        order= Order.objects.filter(customer__name = customer, status = 'Sent').last()
        print(customer)
        print(order)
    else:
        category = Category.objects.all().order_by("name")

    context = {
        'category':category,
        'order':order
    }
    return render(request,'Bakerys/HomePage.html',context)


def MenuDetails(request,menu_id):
    menu = Category.objects.get(id = menu_id)
    category = Category.objects.all().order_by("name")
    item = Item.objects.filter(category__id = menu_id)
    all_user = User.objects.values_list('username',flat=True)
    print(all_user)

    
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
    return render(request,'Bakerys/MenuDetails.html',context)



