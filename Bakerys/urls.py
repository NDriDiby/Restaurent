from django.contrib import admin
from django.urls import path,include
from. import views
from .models import OrderBakerys

app = OrderBakerys._meta.app_label+"?table=14"

urlpatterns = [
    path('bakerys/', views.HomePageBakerys,name='homepage-bakerys'),
    path('bakerys/menudetails/<menu_id>/', views.MenuDetailsBakerys,name='menu_details-bakerys'),
    path('bakerys/myorder/', views.MyOrderBakerys,name='order-bakerys'),
    path('bakerys/sendorder/', views.SendOrderBakerys, name='send_order-bakerys'),
    path('bakerys/updateitem/', views.UpdatedItemBakerys, name='update_item-bakerys'),
    path('bakerys/cuisine/', views.CuisineBakerys, name='cuisine-bakerys'),
    path('bakerys/deleteorder/<item_id>/',views.DeleteOrderBakerys, name='delete_order-bakerys'),

]