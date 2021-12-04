from django.db import models
from accounts.models import Account
from store.models import Product,Variation


# Create your models here.
STATUS = (
    (1,'Order Accepted'),
    (2,'Shipped'),
    (3,'Out For Delivery'),
    (4,'Deliverd'),
    (0,'cancelled'),
)
PAYMENT_METHOD=(
    ('cash_on_delivery','cash_on_delivery'),
    ('paypal','paypal'),
    ('rezorpay','rezorpay'),
)
class Payment(models.Model):
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=200)
    payment_method = models.CharField(max_length=200)
    amount_paid = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment_id

class Order(models.Model):
    user = models.ForeignKey(Account,on_delete=models.SET_NULL,null=True)
    payment = models.ForeignKey(Payment,on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    pincode = models.CharField(max_length=20)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    landmark = models.CharField(max_length=200)
    alternate_phone = models.CharField(max_length=200)
    order_number = models.CharField(max_length=200)
    order_total = models.FloatField()
    tax = models.FloatField()
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True,default=None)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    status = models.IntegerField(choices=STATUS,default=1)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product.product_name
  
    
class Address(models.Model):
    TYPE=(
        ('home','home'),
        ('work','work'),
    )
    user = models.ForeignKey(Account,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)
    pincode = models.CharField(max_length=20)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    landmark = models.CharField(max_length=200)
    alternate_phone = models.CharField(max_length=200)
    type = models.CharField(max_length=200,choices=TYPE)
    