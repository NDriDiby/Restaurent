
from django.contrib import admin
from django.urls import path,include
from Customer import views as cust_view
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('register/', cust_view.RegisterCustomer,name='register'),
    path('login/',cust_view.Login,name = 'login'),
    path('logout/',cust_view.Logout,name = 'logout')


]