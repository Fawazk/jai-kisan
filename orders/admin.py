from django.contrib import admin
from . models import Address, Order,Payment,OrderProduct

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'name', 'phone','city', 'order_total', 'tax','is_ordered', 'created_at']
    list_filter = ['is_ordered']
    search_fields = ['order_number', 'name','phone']
    list_per_page = 20
    # inlines = [OrderProductInline]
admin.site.register(Order,OrderAdmin)
admin.site.register(Payment)
admin.site.register(OrderProduct)
admin.site.register(Address)