from django.forms import ModelForm

# local
from .models import CategoryOffer, Coupon, ProductOffer

class ProductOfferForm(ModelForm):

    class Meta:
        model = ProductOffer
        fields = ['product', 'discount_offer', 'is_active']
        
class CategoryOfferForm(ModelForm):

    class Meta:
        model = CategoryOffer
        fields = ['category', 'discount_offer', 'is_active']

class CouponForm(ModelForm):
    class Meta:
        model = Coupon
        fields = ['coupon_code','discount','is_active']