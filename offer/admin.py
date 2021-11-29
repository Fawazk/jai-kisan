from django.contrib import admin
from offer.models import CategoryOffer, ProductOffer

# Register your models here.

admin.site.register(ProductOffer)
admin.site.register(CategoryOffer)