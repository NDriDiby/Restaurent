from django.shortcuts import render,redirect
from .models import Category,OrderBakerys,ItemBakerys,OrderItemBakerys,CustomerBekerys
import json
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http.response import HttpResponseRedirect,JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import permission_required,login_required


# Create your views here.
def HomePage(request):
    order = None
    category = Category.objects.all().order_by("name")
    if request.user.is_authenticated:
        customer = request.user
        print(customer)
        cust,created = CustomerBekerys.objects.get_or_create(user =request.user)
        order= OrderBakerys.objects.filter(customer = cust, status = 'Sent').last()
        
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
    item = ItemBakerys.objects.filter(category__id = menu_id)
    all_user = User.objects.values_list('username',flat=True)
    

    if request.user.is_authenticated:
        username = User.objects.get(id=request.user.id)
        cust,created = CustomerBekerys.objects.get_or_create(user =request.user)
        cust.name = username.username
        cust.save()
        order,created= OrderBakerys.objects.get_or_create(customer=cust,status='Pending')
        cartItem = order.get_order_quantity()
    

    else:
        return HttpResponseRedirect('/register/')

        
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


def MyOrder(request):
    if request.user.is_authenticated:
        cust,created = CustomerBekerys.objects.get_or_create(user =request.user)
        order,created= OrderBakerys.objects.get_or_create(customer=cust,status='Pending')
        items = order.orderitembakerys_set.all()
        cartItem = order.get_order_quantity()

    if request.method == 'POST':
         return redirect('homepage')


    context = {
        'order':order,
        'items':items,
        'cart_quantity':cartItem}    
    return render(request,'Bakerys/MyOrder.html',context)



def UpdatedItem(request):
    data = json.loads(request.body)
    itemId = data['itemId']
    action = data['action']

    print('ItemId:',itemId)
    print('action:',action)

    
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

    return JsonResponse(f'Item  {action}',safe=False)
    


@csrf_protect
def SendOrder(request):
    data = json.loads(request.body)
    action = data['action']
    order_numb = data['order']
    print('status:',action)
    print('order_number:',order_numb)

    if request.method == 'POST' and action == 'sent':
        cust,created = CustomerBekerys.objects.get_or_create(user =request.user)
        order = OrderBakerys.objects.filter(customer = cust).last()
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
        order = OrderBakerys.objects.get(id = order_numb)
        order.status = 'Completed'
        order.complete = True
        order.save()
        print('completed order')
    
    return JsonResponse("Order Sent",safe=False)




@csrf_protect
@login_required
@permission_required('Resto.view_order',login_url='/login/')
def Cuisine(request):


    all_order = OrderBakerys.objects.filter(status='Sent')
    complete_order = OrderBakerys.objects.filter(complete=True)
    
    context = {
        'all_order':all_order,
        'complete':complete_order
    }
    return render(request,'Bakerys/Cuisine.html',context)