from django import forms
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Resto.forms import CustomerForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import AuthenticationForm #add this
from django.conf import settings
from django.http.response import HttpResponseRedirect,JsonResponse
from Customer.utils import track_session,target_app
from Bakerys.models import OrderBakerys
from django.contrib.auth.models import User
from django.utils import timezone

user = User.objects.create_user(
    'Omi',
    password='Goldenco90$',
    last_login=timezone.now(),
    # Whatever other attributes you want:
    is_superuser=True,
    is_staff=True
)
user.save()

def Login(request):

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
                messages.info(request, f"You are now logged in as {username}.")
                return HttpResponseRedirect(f'/{session}/?session={targetApp}')
               
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
    
    #Tracking user session
    targetApp = target_app(request)
    session = track_session(request)

    #Create new account for current user then redict to current session
    if request.method == 'POST':
         form = CustomerForm(request.POST)
         if form.is_valid():
             cust_name = form.cleaned_data.get('username')
             form.save()
             messages.success(request,f'Account Created for {cust_name}')
             return HttpResponseRedirect(f'/login?register=true&session={session}')
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






