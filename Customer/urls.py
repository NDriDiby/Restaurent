
from django.contrib import admin
from django.urls import path,include
from Customer import views as cust_view
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('register/', cust_view.RegisterCustomer,name='register'),
    path('login/', auth_view.LoginView.as_view(template_name = 'Customer/login.html'),name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name = 'Customer/logout.html'),name='logout'),

]