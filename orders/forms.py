from django import forms
from django.forms import fields

from .models import Order,Address, OrderProduct


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name','phone','address','pincode','locality','landmark','city','state','alternate_phone']
        
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields =['name','phone','address','pincode','locality','landmark','city','state','alternate_phone','type']
    
    def __init__(self, *args, **kwargs):
        super(AddressForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            
class OrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ['user','payment','product','quantity','product_price','status']            
            
            
