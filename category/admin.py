from django.contrib import admin

from category.models import category

# Register your models here.


class categoryAdmin(admin.ModelAdmin):
    prepopulated_fields ={'slug':('category_name',)}
    list_display = ('category_name','slug')
admin.site.register(category,categoryAdmin)
