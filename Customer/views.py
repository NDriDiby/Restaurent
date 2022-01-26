from django import forms
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Resto.forms import CustomerForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm #add this
from django.conf import settings
from django.http.response import HttpResponseRedirect,JsonResponse
from Customer.utils import track_session,target_app,get_table_number
from Bakerys.models import OrderBakerys
from django.contrib.auth.models import User
from django.utils import timezone
from Resto.models import Customer



def Login(request):
    
    #Table Number
    table = get_table_number(request)
    if table == None:
        pass

    #Tracking user session
    targetApp = target_app(request)
    session = track_session(request)
    print('my current sess:',session)

    #Authenticate user then redict to their session
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.has_perm('resto.view_order'):
                    return HttpResponseRedirect(f'/texasgrillz/cuisine/')
                else:
                    messages.info(request, f"You are now logged in as {user.first_name}")
                    return HttpResponseRedirect(f'/{session}/?session={targetApp}')
        else:
            messages.warning(request, f"Username and password didn't match")
                
               
    else:
        form = AuthenticationForm()

    context = {
        'form':form,
        'app':targetApp
        }

    return render(request,'Customer/Login.html',context)



#Logout
def Logout(request):

    #Tracking user session 
    targetApp = target_app(request)
    session = track_session(request)
    
    #LogOut current user
    logout(request)
    context = {
        'session':session,
        'app':targetApp
    }
    
    return render (request,'Customer/Logout.html',context)


#Register new user
def RegisterCustomer(request):
    
    #Table Number
    table = get_table_number(request)
    if table == None:
        pass
    
    #Tracking user session
    targetApp = target_app(request)
    session = track_session(request)

    #Create new account for current user then redict to current session
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            cust_name = form.cleaned_data.get('username')
            cust_first_name = form.cleaned_data.get('prenom')
            cust_last_name = form.cleaned_data.get('nom')
            cust_email = form.cleaned_data.get('email')
            cust_phone = form.cleaned_data.get('phone_number')
            form.save()
            user,created= User.objects.get_or_create(username = cust_name)
            user.first_name = cust_first_name
            user.last_name = cust_last_name 
            user.email = cust_name
            user.phone_number = cust_phone
            user.save()
            messages.success(request,f'Account Created for {cust_first_name} {cust_last_name}')
            return HttpResponseRedirect(f'/login/?register=true&session={targetApp}')
        else:
            messages.warning(request,f"The two password fields didn’t match")
            
    else:
        form = CustomerForm()
       

    context={
        'form':form,
        'session':session,
        'app':targetApp
    }
    return render(request,'Customer/Register.html',context)



#Profile
@login_required(login_url='/login/')
def Profile(request):
    return render(request,'Customer/Profile.html')






