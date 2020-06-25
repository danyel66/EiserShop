from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)

class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'add1',
        'name': 'add1'
    }))
    apartment_address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'add2',
        'name': 'add2'
    }))
    country = CountryField(blank_label='Select Country').formfield(
        widget=CountrySelectWidget(attrs={
            'class': 'country_select'
        }))
    number = forms.IntegerField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'number',
        'name': 'number'

    }))
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'city',
        'name': 'city'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'zip',
        'placeholder': 'Postcode/ZIP'
    }))
    same_shipping_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, choices=PAYMENT_CHOICES
    )
