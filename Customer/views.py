from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from Resto.forms import CustomerForm
from django.contrib import messages

# Create your views here.
#register new user


def RegisterCustomer(request):
    if request.method == 'POST':
         form = CustomerForm(request.POST)
         if form.is_valid():
             cust_name = form.cleaned_data.get('username')
             messages.success(request,f'Account Created for {cust_name}')
             return redirect('homepage')
    else:
        form = CustomerForm()

    context={
        'form':form
    }
    return render(request,'Customer/Register.html',context)


#Profile
@login_required
def Profile(request):
    return render(request,'Customer/Profile.html')






