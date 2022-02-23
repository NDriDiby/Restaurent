
from django.contrib import admin
from django.urls import path,include
from Customer import views as cust_view
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('register/', cust_view.RegisterCustomer,name='register'),
    path('login/',cust_view.Login,name = 'login'),
    path('logout/',cust_view.Logout,name = 'logout'),
    path('password_reset/',auth_view.PasswordResetView.as_view(template_name = 'Customer/password_reset.html',
    html_email_template_name = "Customer/password_reset_email.txt",extra_email_context ={'page':'password_reset/'}),name = 'password_reset'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='Customer/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view(template_name="Customer/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_view.PasswordResetCompleteView.as_view(template_name='Customer/password_reset_complete.html'), name='password_reset_complete'),   
    path('noaccess/',cust_view.NoAccess,name = 'no_access')


]