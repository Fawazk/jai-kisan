from django.db import models
from category.models import category
from django.contrib.auth import get_user_model

# Create your models here.


class ProductOffer(models.Model):
    product = models.OneToOneField('store.Product', on_delete=models.CASCADE)
    discount_offer = models.PositiveIntegerField(help_text='Offer in percentage')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.discount_offer)
    
    
class CategoryOffer(models.Model):
    category = models.OneToOneField(category, on_delete=models.CASCADE)
    discount_offer = models.PositiveIntegerField(help_text='Offer in percentage')
    is_active = models.BooleanField(default=True)
    
    
    def __str__(self):
        return str(self.discount_offer)
    
class Coupon(models.Model):
    coupon_name = models.CharField(max_length=50)
    coupon_code = models.CharField(max_length=50, unique=True)
    discount = models.PositiveIntegerField(help_text="Offer in percentage", null=True)
    limit = models.PositiveIntegerField()
    used = models.PositiveIntegerField(default=0)
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.coupon_name


class RedeemedCoupon(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.email} - {self.coupon.coupon_name}'