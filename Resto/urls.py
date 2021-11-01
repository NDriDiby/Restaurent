from django.contrib import admin
from django.urls import path,include
from. import views

urlpatterns = [
    path('', views.HomePage,name='homepage'),
    path('menudetails/<menu_id>/', views.MenuDetails,name='menu_details'),
    path('myorder/', views.MyOrder,name='order'),
    path('updateitem/', views.UpdatedItem, name='update_item'),

]