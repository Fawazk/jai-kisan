from django.contrib import admin
from offer.models import CategoryOffer, Coupon, ProductOffer, RedeemedCoupon

# Register your models here.

admin.site.register(ProductOffer)
admin.site.register(CategoryOffer)
admin.site.register(Coupon)
admin.site.register(RedeemedCoupon)