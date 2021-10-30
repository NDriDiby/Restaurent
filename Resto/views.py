from django.shortcuts import render
from.models import Category

# Create your views here.

def HomePage(request):
    category = Category.objects.all()

    context = {
        'category':category,
    }
    return render(request,'Resto/HomePage.html',context)


def MenuDetails(request,menu_id):
    
    menu = Category.objects.get(id = menu_id)
    category = Category.objects.all()

    context = {
        'menu':menu,
        'category':category
    }

    return render(request,'Resto/MenuDetails.html',context)
