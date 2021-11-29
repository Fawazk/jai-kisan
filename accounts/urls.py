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
    path('resent_otp',views.resent_otp,name="resent_otp"),
    path('new_password',views.new_password,name='new_password'),
    path('confirm_register_otp',views.confirm_register_otp,name='confirm_register_otp'),
    path('resent_register_otp',views.resent_register_otp,name="resent_register_otp"),
    path('logout',views.logout,name="logout"),
    # ----------------------------------------
    path('profile',views.profile,name='profile'),
    path('edit_profile/<int:id>/',views.edit_profile,name='edit_profile'),
    path('change_password',views.change_password,name="change_password"),
    path('address_management',views.address_management,name='address_management'),
    path('edit_address/<int:id>/',views.edit_address,name='edit_address'),
    path('cancel_address/<int:id>/',views.cancel_address,name='cancel_address'),
    path('add_address',views.add_address,name='add_address'),
]