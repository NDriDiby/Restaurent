from django.contrib import admin
from django.urls import path,include
from. import views

urlpatterns = [
    path('texasgrillz/', views.HomePage,name='homepage-texasgrillz'),
    path('texasgrillz/menudetails/<menu_id>/', views.MenuDetails,name='menu_details-texasgrillz'),
    path('texasgrillz/myorder/', views.MyOrder,name='order-texasgrillz'),
    path('texasgrillz/itemdetails/<item_id>/', views.ItemDetails, name='item_details-texasgrillz'),
    path('texasgrillz/updateitem/', views.UpdatedItem, name='update_item-texasgrillz'),
    path('texasgrillz/sendorder/', views.SendOrder, name='send_order-texasgrillz'),
    path('texasgrillz/cuisine/', views.Cuisine, name='cuisine-texasgrillz'),
    path('texasgrillz/deleteorder/<item_id>/',views.DeleteOrder, name='delete_order-texasgrillz'),
    path('texasgrillz/inventory/',views.IventorySystem, name='inventory-texasgrillz'),
    path('texasgrillz/settings/',views.CuisineSettings, name='settings-texasgrillz'),

]


