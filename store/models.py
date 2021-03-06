from django.db import models
from django.db.models.aggregates import Sum
from django.db.models.deletion import CASCADE
from category.models import category
from django.urls import reverse
from accounts.models import Account
from django.db.models import Avg
from django.utils import timezone
from django.apps import apps
# Create your models here.
class Product(models.Model):
    product_name  = models.CharField(max_length=200, unique=True)
    slug          = models.SlugField(max_length=200, unique=True)
    description   = models.TextField(max_length=200,blank=True)
    price         = models.IntegerField(null=True)
    tax           = models.IntegerField(null=True)
    images_one    = models.ImageField(upload_to='images/products',blank=True)
    images_two    = models.ImageField(upload_to='images/products',blank=True)
    images_three  = models.ImageField(upload_to='images/products',blank=True)
    stock         = models.IntegerField()
    is_available  = models.BooleanField(default=True)
    p_category    = models.ForeignKey(category,on_delete=models.CASCADE)
    create_date   = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    
    def get_url(self):
        return reverse('product_detail',args=[self.p_category.slug, self.slug])
    def get_price(self):
        try:
            if self.productoffer.is_active:
                offer_price = (self.price / 100) * self.productoffer.discount_offer
                p_price = self.price - offer_price
                return p_price
            raise
        except:
            try:
                if self.p_category.categoryoffer.is_active:
                    offer_price = (self.price / 100) * self.p_category.categoryoffer.discount_offer
                    p_price = self.price - offer_price
                    return p_price
                raise
            except:
                pass
            return self.price
    
    def averageReview(self):
        reviews = ReviewRating.objects.filter(product=self,status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
            return avg
    
    def __str__(self):
        return self.product_name
    
    def get_revenue(self,month=timezone.now().month):
        
        orderproduct = apps.get_model('orders', 'OrderProduct')
        orders=orderproduct.objects.filter(product=self,created_at__month=month,status=4)
        return orders.values('product').annotate(revenue=Sum('product_price'))
    def get_profit(self,month=timezone.now().month):
        
        orderproduct = apps.get_model('orders', 'OrderProduct')
        orders=orderproduct.objects.filter(product=self,created_at__month=month,status=4)
        profit_calculted=orders.values('product').annotate(profit=Sum('product_price'))
        profit_calculated=profit_calculted[0]['profit']*0.23
        return profit_calculated
    def get_count(self,month=timezone.now().month):
        orderproduct = apps.get_model('orders', 'OrderProduct')
        orders=orderproduct.objects.filter(product=self,created_at__month=month,status=4)
        return orders.values('product').annotate(quantity=Sum('quantity'))
        
    
variation_category_choice =(

    ('age','age'),
)
class Variation(models.Model):
    product            = models.ForeignKey(Product, on_delete=models.CASCADE)
    # price              = models.IntegerField(default=100)
    variation_category = models.CharField(max_length=200, choices=variation_category_choice)
    variation_value    = models.CharField(max_length=200)
    is_active          = models.BooleanField(default=True)
    create_date        = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return self.variation_value
    
class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject