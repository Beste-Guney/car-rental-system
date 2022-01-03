from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.db import connection

class UserLoginForm(forms.Form):
    email = forms.EmailField(label='Enter email')
    password = forms.CharField(label='Enter your password', widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})


class CustomerCreationForm(forms.Form):
    LICENSE_TYPES = (("A1", 'A1'), ("A2", 'A2'), ("A", 'A'), ("M", 'M'), ("B1",'B1'), ("B",'B'), ("BE", 'BE'), ("C1",'C1'), ("C", 'C'), ("CE", 'CE'))

    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput, min_length=6)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput, min_length=6)
    phone_number = forms.CharField(label='phone_number', max_length=100)
    address = forms.CharField(label='adress', max_length=100)
    state = forms.CharField(label='nationality', max_length=20)
    #birth_date = forms.DateField(label='birthday', widget=forms.DateInput(attrs={'placeholder': '__/__/____', 'class': 'date',}))
    #info about license of the user
    license_number = forms.IntegerField(label='license_number')
    license_type = forms.ChoiceField(choices=LICENSE_TYPES, label='license_type')
    received_date = forms.DateField(label='received date of license', widget=forms.DateInput(format=('%Y-%m-%d'),
        attrs={'class': 'form-control',
               'placeholder': 'Select the date',
               'type': 'date'
              }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field is not 'birth_date':
                self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})


class BranchEmployeeCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput, min_length=6)
    salary = forms.FloatField(label='Salary')
    phone_number = forms.CharField(label='phone_number', max_length=100)
    address = forms.CharField(label='adress', max_length=100)
    branch = forms.IntegerField(label='branch_id')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})


class ChauffeurCreationForm(forms.Form):
    CAR_TYPE = (('sedan', 'sedan'), ('suv', 'suv'), ('limo', 'limo'))

    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput, min_length=6)
    salary = forms.FloatField(label='Salary')
    phone_number = forms.CharField(label='phone_number', max_length=100)
    address = forms.CharField(label='adress', max_length=100)
    years = forms.IntegerField(label='driving_years')
    car_type = forms.ChoiceField(choices=CAR_TYPE)
    branch = forms.IntegerField(label='branch_id')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})


class DamageExpertCreationForm(forms.Form):
    CAR_TYPE = (('sedan', 'sedan'), ('suv', 'suv'), ('limo', 'limo'))

    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput, min_length=6)
    salary = forms.FloatField(label='Salary')
    phone_number = forms.CharField(label='phone_number', max_length=100)
    address = forms.CharField(label='adress', max_length=100)
    car_type = forms.ChoiceField(choices=CAR_TYPE)
    branch = forms.IntegerField(label='branch_id')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})


class ManagerCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password = forms.CharField(label='Enter password', widget=forms.PasswordInput, min_length=6)
    phone_number = forms.CharField(label='phone_number', max_length=100)
    salary = forms.FloatField(label='Salary')
    address = forms.CharField(label='adress', max_length=100)
    budget = forms.FloatField(label='budget of branch')
    branch_name = forms.CharField(label='name of your branch')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})