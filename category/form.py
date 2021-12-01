from django.db.models import fields
from django.forms import ModelForm
from django import forms
from category.models import category




class CategoryForm(forms.ModelForm):
    class Meta:
        model =  category
        fields = ['category_name','description']
