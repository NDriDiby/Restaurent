from django.contrib import admin
from django.urls import path,include
from. import views

urlpatterns = [
    path('bakerys/', views.HomePage,name='homepage'),
    path('bakerys/menudetails/<menu_id>/', views.MenuDetails,name='menu_details'),
    path('bakerys/myorder/', views.MyOrder,name='order'),
    path('bakerys/sendorder/', views.SendOrder, name='send_order'),
    path('bakerys/updateitem/', views.UpdatedItem, name='update_item'),
    path('bakerys/cuisine/', views.Cuisine, name='cuisine'),
]