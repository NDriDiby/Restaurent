from django import forms
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Resto.forms import CustomerForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm #add this
from django.conf import settings

# Create your views here.


def Login(request):
    apps = [appname.split('.')[0] for appname in settings.INSTALLED_APPS if 'Config' in appname]
    for app in range(0,len(apps)):
        if apps[app] in request.session:
            print('Login App Name:',apps[app])
            
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('homepage-bakerys')
       
    else:
        form = AuthenticationForm()
    context = {
         'form':form}

    return render(request,'Customer/Login.html',context)



#register new user
def RegisterCustomer(request):
    if request.method == 'POST':
         form = CustomerForm(request.POST)
         if form.is_valid():
             cust_name = form.cleaned_data.get('username')
             form.save()
             messages.success(request,f'Account Created for {cust_name}')
             return redirect('login')
    else:
        form = CustomerForm()

    context={
        'form':form
    }
    return render(request,'Customer/Register.html',context)



#Profile
@login_required(login_url='/login/')
def Profile(request):

    return render(request,'Customer/Profile.html')






