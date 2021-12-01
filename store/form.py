from django.db.models import fields
from django.forms import ModelForm
from .models import Product
from .models import ReviewRating
from django import forms
class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_name','price','images_one','images_two','images_three','description','tax','stock','is_available','p_category']
              
class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ['subject', 'review', 'rating']