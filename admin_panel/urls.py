from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminpanel,name='adminpanel'),
    path('admin_dashboard',views.admin_dashboard,name="admin_dashboard"),
    path('category_list',views.category_list,name='category_list'),
    path('Product_list',views.Product_list,name='Product_list'),
    path('deleteproduct/<cat_id>', views.deleteproduct,name='deleteproduct'),
    path('deletecategory/<cat_id>', views.deletecategory,name='deletecategory'),
    path('editcategory/<cat_id>', views.editcategory,name='editcategory'),
    path('addcategory',views.addcategory,name='addcategory'),
    path('addProduct',views.addProduct,name='addProduct'),
    path('editproduct/<cat_id>',views.editproduct,name='editproduct'),
    path('user_list',views.user_list,name='user_list'),
    path('deleteuser/<user_id>',views.deleteuser,name='deleteuser'),
    path('blockuser/<user_id>',views.blockuser,name='blockuser'),
    path('unblockuser/<user_id>',views.unblockuser,name='unblockuser'),
    path('order_list',views.order_list,name='order_list'),
    path('edit_order/<int:order_product_id>/',views.order_edit,name='order_edit'),
    path('order_history',views.order_history,name='order_history'),
    path('product_offer',views.product_offer,name='product_offer'),
    path('deleteproductoffer/<int:offer_id>/',views.deleteproductoffer,name="deleteproductoffer"),
    path('editproductoffer/<int:offer_id>/',views.editproductoffer,name="editproductoffer"),
    path('add_productoffer',views.add_productoffer,name="add_productoffer"),
    
    
    path('category_offer',views.category_offer,name="category_offer"),
    path('deletecategoryoffer/<int:offer_id>/',views.deletecategoryoffer,name='deletecategoryoffer'),
    path('editcategoryoffer/<int:offer_id>/',views.editcategoryoffer,name="editcategoryoffer"),
    path('add_categoryoffer',views.add_categoryoffer,name='add_categoryoffer'),
    ]