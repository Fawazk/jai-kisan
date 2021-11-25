from django.contrib import admin
from django.db import models
from .models import Product,Variation,ReviewRating
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','stock','p_category','price','modified_date','is_available')
    prepopulated_fields = {'slug':('product_name',)}
    
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value')

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRating)

