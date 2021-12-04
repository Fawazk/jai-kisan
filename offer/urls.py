from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('apply_coupon',views.apply_coupon,name="apply_coupon"),
]