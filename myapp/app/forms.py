from django import forms
from .models import Customer, ShippingAddress

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email','phone','country', 'city','postal_code','profile_picture']

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email address'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone number'  }),
            'country': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Country'}),
            'city': forms.TextInput(attrs={'class': 'form-control','placeholder': 'City' }),
            'postal_code': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Postal code'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control' }),}



class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['full_name', 'address_line']