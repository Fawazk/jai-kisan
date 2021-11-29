from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('place_order/',views.place_order,name='place_order'),
    path('payments',views.payments,name='payments'),
    path('order_complete',views.order_complete,name='order_complete'),
    
    
    path('orderdetails/<int:order_id>/',views.orderdetails,name="orderdetails"),
    path('my_orders',views.my_orders,name="my_orders"),
    path('cancel_order/<int:order_id>/',views.cancel_order,name='cancel_order'),

]