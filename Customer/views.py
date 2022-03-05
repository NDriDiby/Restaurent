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
    # phone = request.GET.get('phone')
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
                    messages.info(request, f"Vous êtes maintenant connecté en tant que {user.first_name}")
                    return HttpResponseRedirect(f'/{session}/?session={targetApp}')
        else:
            messages.warning(request, f"Le nom d'utilisateur et le mot de passe ne correspondent pas")
            
                
               
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
    
    
    #My Testeur
    testeur = User.objects.values_list('username',flat=True)
    print(testeur)
    
    
    
    

    #Create new account for current user then redict to current session
    if request.method == 'POST':
        form = CustomerForm(request.POST or None)
        print(form.errors)
        
        
        if 'ndiby65@gmail.com' in testeur:
            print("YES")
        
        if form.is_valid():
            cust_log_email = form.cleaned_data.get('username')
            cust_first_name = form.cleaned_data.get('prenom')
            cust_last_name = form.cleaned_data.get('nom')
            cust_phone = form.cleaned_data.get('phone_number')
            
            
            if (cust_log_email in ['ndiby65@gmail.com','icarus@gmail.com','kaxharel@gmail.com','felinspiritual508@gmail.com',
                                   'zeynabfdg02@gmail.com','sostheneange@gmail.com','wogninroger86@gmail.com','ohachosimjennifer@gmail.com',
                                   'htehua07@gmail.com','rickysilencieux@gmail.com','sinoussouc@gmail.com','tkfatim@gmail.com','bakayokohassan112@gmail.com',
                                   'cedric.acho@gmail.com','yedofficiel@gmail.com','yannis_kodjo@yahoo.com','cyrayacine@gmail.com','seydinaibrahim16@gmail.com',
                                   'salimatabamba37@gmail.com','diarrassoumar@outlook.com','nbrandon@hotmail.fr']):
                form.save() #User created 
                user,created= User.objects.get_or_create(username = cust_log_email)
                user.first_name = cust_first_name
                user.last_name = cust_last_name 
                user.email = cust_log_email
                user.save()
                messages.success(request,f'Compte créé pour {cust_first_name} {cust_last_name}')
                
                newline = "\n"
                #send email after registration
                send_mail("Bienvenue sur Icarus",
                          f"Salut {cust_first_name},{newline}{newline}Bienvenu sur Icarus Bar & Restaurent et merci d'utiliser notre service. Nous sommes très heureux de vous compter parmis nos utilisateurs.\
                          {newline}{newline}Meilleurs Salutations.{newline}Nova Cloud Team",
                          settings.EMAIL_HOST_USER,
                          [cust_log_email],fail_silently=False,)
                
                return HttpResponseRedirect(f'/login/?register=true&session={targetApp}') #send to login page
            
                
            
            elif (cust_log_email not in testeur): #retrict access
                return HttpResponseRedirect(f'/noaccess/')
            
            
            
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



def csrf_failure(request,reason=" no token"):
    
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
    
    return render(request,'Customer/csrf_token_error.html',context)


# def PasswordResetRequest(request):
# 	if request.method == "POST":
# 		password_reset_form = PasswordResetForm(request.POST)
# 		if password_reset_form.is_valid():
# 			data = password_reset_form.cleaned_data['email']
# 			associated_users = User.objects.filter(Q(email=data))
# 			if associated_users.exists():
# 				for user in associated_users:
# 					subject = "Password Reset Requested"
# 					email_template_name = "Customer/password_reset_email.txt"
# 					c = {
# 					"email":user.email,
# 					'domain':'127.0.0.1:8000',
# 					'site_name': 'Website',
# 					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
# 					"user": user.first_name,
# 					'token': default_token_generator.make_token(user),
# 					'protocol': 'http',
# 					}
# 					email = render_to_string(email_template_name, c)
# 					try:
# 						send_mail(subject, email, 'prudencediby@gmail.com' , [user.email], fail_silently=False)
# 					except BadHeaderError:
# 						return HttpResponse('Invalid header found.')
# 					return redirect ("/password_reset/done/")
# 	password_reset_form = PasswordResetForm()
# 	return render(request,"Customer/password_reset.html", context={"password_reset_form":password_reset_form})






