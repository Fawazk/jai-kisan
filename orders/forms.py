from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['name','phone','address','pincode','locality','city','state','landmark','alternate_phone']