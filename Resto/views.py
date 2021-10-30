from django.shortcuts import render
from.models import Category,Item

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

    context = {
        'menu':menu,
        'category':category,
        'item':item
    }

    return render(request,'Resto/MenuDetails.html',context)
