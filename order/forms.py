from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.contrib.auth.models import User

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    apartment_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    country = CountryField(blank_label='Select Country').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'country_select'
        }))
    number = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control',

    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    same_shipping_address = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES
    )


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact_form',
        'placeholder': 'Coupon Code'
    }))
