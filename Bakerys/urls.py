from django.contrib import admin
from django.urls import path,include
from. import views

urlpatterns = [
    path('bakerys/homepage/', views.HomePage,name='homepage'),
    path('bakerys/menudetails/<menu_id>/', views.MenuDetails,name='menu_details')
]