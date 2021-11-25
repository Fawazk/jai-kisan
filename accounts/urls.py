from os import name
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('register',views.register,name='register'),
    path('signin',views.signin,name='signin'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('otp',views.otp,name='otp'),
    path('new_password',views.new_password,name='new_password'),
    path('confirm_register_otp',views.confirm_register_otp,name='confirm_register_otp'),
    path('logout',views.logout,name="logout"),
    # ----------------------------------------
    path('account',views.account,name='account'),
    path('my_orders',views.my_orders,name="my_orders"),
]