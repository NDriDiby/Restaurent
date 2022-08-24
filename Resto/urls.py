from django.contrib import admin
from django.urls import path,include
from. import views

urlpatterns = [
    path('texasgrillz/', views.HomePage,name='homepage-texasgrillz'),
    path('texasgrillz/user_profile/',views.UserProfile,name='user_profile'),
    path('texasgrillz/menudetails/<menu_id>/', views.MenuDetails,name='menu_details-texasgrillz'),
    path('texasgrillz/myorder/', views.MyOrder,name='order-texasgrillz'),
    path('texasgrillz/itemdetails/<item_id>/', views.ItemDetails, name='item_details-texasgrillz'),
    path('texasgrillz/sidedetails/<side_id>/', views.SideDetails, name='side_details-texasgrillz'),
    path('texasgrillz/updateitem/', views.UpdatedItem, name='update_item-texasgrillz'),
    path('texasgrillz/checkoutpage/', views.CheckoutPageUpdate, name='checkoutpage-texasgrillz'),
    path('texasgrillz/sendorder/', views.SendOrder, name='send_order-texasgrillz'),
    path('texasgrillz/cuisine/', views.Cuisine, name='cuisine-texasgrillz'),
    path('texasgrillz/deleteitem/',views.DeleteItem, name='delete_item-texasgrillz'),#Backend process
    path('texasgrillz/deleteorderitem/',views.DeleteOrderItem, name='delete_order_item-texasgrillz'),
    path('texasgrillz/inventory/',views.IventorySystem, name='inventory-texasgrillz'),
    path('texasgrillz/settings/',views.CuisineSettings, name='settings-texasgrillz'),
    path('texasgrillz/GetOrderCuisine/',views.GetOrderCuisine, name='GetOrderCuisine'),
    path('texasgrillz/CompletedOrder/',views.CompletedOrder, name='completed_order'),
    path('texasgrillz/cuisineOptimize/', views.CuisineOptimize, name='cuisine-texasgrillz-optimize'),
    path('texasgrillz/analytics/', views.Analytics, name='texasgrillz-analytics'),
    path('texasgrillz/revenues/', views.Revenues, name='texasgrillz-revenues'),
    path('texasgrillz/menuDetailsData/<menu_id>', views.MenuDetailsData, name='item_details_data-texasgrillz'),
    path('cinetpayapi/',views.CinetPayCredential,name='cinetpayapi'),#Backend process
    path('process_transaction/',views.ProcessTransaction,name='process_transaction'), #Backend process
    path('texasgrillz/dashBoard_data/',views.DashBoardData, name ='dashboard_data'),
    
]


