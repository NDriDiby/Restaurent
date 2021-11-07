from django.contrib import admin
from django.urls import path,include
from. import views

urlpatterns = [
    path('', views.HomePage,name='homepage'),
    path('menudetails/<menu_id>/', views.MenuDetails,name='menu_details'),
    path('myorder/', views.MyOrder,name='order'),
    path('processauth/', views.ProcessOrder,name='process_order'),
    path('updateitem/', views.UpdatedItem, name='update_item'),
    path('sendorder/', views.SendOrder, name='send_order'),
    path('cuisine/', views.Cuisine, name='cuisine'),
    path('deleteorder/<item_id>',views.DeleteOrder, name='delete_order'),

]