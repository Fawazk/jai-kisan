from django import forms
from django.forms import fields
from .models import Account, Banner

class RegisterationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confirm Password',
    }))
    phone_number = forms.CharField(label='Mobile', required=True, widget=forms.NumberInput)
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email','phone_number','password']
        
        
    def __init__(self,*args,**kwargs):
        super(RegisterationForm, self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['password'].widget.attrs['placeholder'] = 'Enter Password'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Confirm Password'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            
            
    def clean(self):
        cleaned_data = super(RegisterationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password != confirm_password:
            raise forms.ValidationError(
                "password does not match"
            )
            
class edit_profileForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name','last_name','email','phone_number','profile_img','state','city']
        
class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['image','description']

    
