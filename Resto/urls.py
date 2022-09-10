from django.contrib import admin
from django.urls import path,include
from. import views

urlpatterns = [
    path('homepage/', views.HomePage,name='homepage'),
    path('user_profile/',views.UserProfile,name='user_profile'),
    path('menudetails/<menu_id>/', views.MenuDetails,name='menu_details'),
    path('myorder/', views.MyOrder,name='order'),
    path('itemdetails/<item_id>/', views.ItemDetails, name='item_details'),
    path('sidedetails/<side_id>/', views.SideDetails, name='side_details'),
    path('updateitem/', views.UpdatedItem, name='update_item'),
    path('checkoutpage/', views.CheckoutPageUpdate, name='checkoutpage'),
    path('sendorder/', views.SendOrder, name='send_order'),
    path('dashboard/', views.DashBoard, name='dashboard'),
    path('deleteitem/',views.DeleteItem, name='delete_item'),#Backend process
    path('deleteorderitem/',views.DeleteOrderItem, name='delete_order_item'),
    path('recipe/',views.Recipe, name='recipe'),
    path('recette/',views.Recette, name='recette'),#Backend Process
    path('settings/',views.Settings, name='settings'),
    path('GetOrderCuisine/',views.GetOrderCuisine, name='GetOrderCuisine'),
    path('CompletedOrder/',views.CompletedOrder, name='completed_order'),
    path('cuisine/', views.Cuisine, name='cuisine'),
    path('analytics/', views.Analytics, name='analytics'),
    path('revenues/', views.Revenues, name='revenues'),
    path('menuDetailsData/<menu_id>', views.MenuDetailsData, name='item_details_data'),
    path('cinetpayapi/',views.CinetPayCredential,name='cinetpayapi'),#Backend process
    path('process_transaction/',views.ProcessTransaction,name='process_transaction'), #Backend process
    path('dashBoard_data/',views.DashBoardData, name ='dashboard_data'),
    
]


