from django import forms


class RegistrationForm(forms.Form):
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    phone = forms.CharField(label='Phone Number', max_length=100)
    password = forms.CharField(label='Password', max_length=100)


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100)


class PaymentForm(forms.Form):
    amount = forms.CharField(label='Amount', max_length=100)
    payment_status = forms.CharField(label='Payment Status', max_length=100)
    payment_type = forms.CharField(label='Payment Type', max_length=100)


class CargoForm(forms.Form):
    delivery_address = forms.CharField(label='Delivery Address', max_length=100)
    delivery_status = forms.CharField(label='Delivery Status', max_length=100)
