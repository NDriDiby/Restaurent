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
from django.contrib.auth.models import User
from django.utils import timezone
from Resto.models import Customer
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import send_mail


def Login(request):
    
    #Table Number
    table = get_table_number(request)
    if table == None:
        pass

    #Tracking user session
    targetApp = target_app(request)
    session = track_session(request)
   
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
                    return HttpResponseRedirect(f'/cuisine/')
                else:
                    return HttpResponseRedirect(f'/homepage/?session={targetApp}')
        else:
            messages.warning(request, f"Le nom d'utilisateur et le mot de passe ne correspondent pas")
            
    else:
        form = AuthenticationForm()
        if 'connected' in request.GET:
            print('WTF')
        

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
    
    
    #My Testeur
    testeur = User.objects.values_list('username',flat=True)
    print(testeur)
    
    
    #Create new account for current user then redict to current session
    if request.method == 'POST':
        form = CustomerForm(request.POST or None)
        
        if form.is_valid():
            cust_log_email = form.cleaned_data.get('username').lower()
            cust_first_name = form.cleaned_data.get('prenom')
            cust_last_name = form.cleaned_data.get('nom')
            cust_phone = form.cleaned_data.get('phone_number')
            form.save() #User created 
            
            user,created= User.objects.get_or_create(username = cust_log_email)
            user.first_name = cust_first_name
            user.last_name = cust_last_name 
            user.email = cust_log_email
            user.save()
            messages.success(request,f'Compte créé pour {cust_first_name} {cust_last_name}')

            
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



def NoAccess(request):
    
    #Table Number
    table = get_table_number(request)
    if table == None:
        pass
    
    #Tracking user session
    targetApp = target_app(request)
    session = track_session(request)
    
    context={
        'session':session,
        'app':targetApp
    }
    
    return render(request,'Customer/No_access.html',context)



# def csrf_failure(request,reason=" no token"):
    
#     #Table Number
#     table = get_table_number(request)
#     if table == None:
#         pass
    
#     #Tracking user session
#     targetApp = target_app(request)
#     session = track_session(request)
    
#     context={
#         'session':session,
#         'app':targetApp
#     }
    
#     return render(request,'Customer/csrf_token_error.html',context)









