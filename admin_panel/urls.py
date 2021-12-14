from os import name
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.adminpanel,name='adminpanel'),
    path('admin_logout',views.admin_logout,name="admin_logout"),
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
    path('coupon_offer',views.coupon_offer,name="coupon_offer"),
    path('coupon_add',views.coupon_add,name="coupon_add"),
    path('edit_coupon/<int:coupon_id>/',views.edit_coupon,name="edit_coupon"),
    path('delete_coupon/<int:coupon_id>/',views.delete_coupon,name='delete_coupon'),
    path('redeemed_coupon',views.redeemed_coupon,name='redeemed_coupon'),
    
    #banner management
    path('banner_list',views.banner_list,name='banner_list'),
    path('add_banner',views.add_banner,name='add_banner'),
    path('banner_edit/<int:banner_id>/',views.banner_edit,name='banner_edit'),
    path('banner_delete/<int:banner_id>/',views.banner_delete,name='banner_delete'),
    
        
    # product_sales
    
    path('product_sales',views.product_sales,name='product_sales'),
    path('download_product_sales_report',views.download_product_sales_report,name='download_product_sales_report'),
    # path('sales_report_pdf',views.sales_report_pdf,name="sales_report_pdf"),
    ]