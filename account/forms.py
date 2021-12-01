from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.db import connection

class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Enter email')
    password = forms.CharField(label='Enter your password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})


class CustomerCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)
    phone_number = forms.CharField(label='phone_number', max_length=100)
    address = forms.CharField(label='adress', max_length=100)
    state = forms.CharField(label='nationality', max_length=20)
    #birth_date = forms.DateField(label='birthday', widget=forms.DateInput(attrs={'placeholder': '__/__/____', 'class': 'date',}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field is not 'birth_date':
                self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})



