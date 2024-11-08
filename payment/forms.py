from django import forms
from .models import ShippingAddress


class PayPalPaymentsForm(forms.Form):
    order_id = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # assign HiddenInput widget      
        self.fields['order_id'].widget = forms.HiddenInput()

class ShippingForm(forms.ModelForm):
	full_name = forms.CharField(label="Full name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full name'}))
	address1 = forms.CharField(label="Address 1", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 1'}))
	address2 = forms.CharField(label="Address 2", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 2'}), required=False)
	city = forms.CharField(label="City", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
	state = forms.CharField(label="State", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}), required=False)
	zipcode = forms.CharField(label="Zipcode", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}))
	country = forms.CharField(label="Country", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}))

	class Meta:
		model = ShippingAddress
		fields = ('full_name', 'address1', 'address2', 'city', 'state', 'zipcode', 'country')


class BillingForm(forms.Form):
	card_name = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name on card'}))
	card_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number'}))
	card_exp_date = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Exp Date'}))
	card_cvv_number = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV'}))
	address1 = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 1'}))
	address2 = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address 2'}))
	city = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}))
	state = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}), required=False)
	zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}))
	country = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Country'}))