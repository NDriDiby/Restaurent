from django.shortcuts import render
from.models import Category

# Create your views here.

def HomePage(request):
    category = Category.objects.all()

    context = {
        'category':category,
    }

    return render(request,'Resto/HomePage.html',context)
