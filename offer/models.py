from django.db import models
from category.models import category


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