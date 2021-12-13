from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, redirect
from django.views import View
from django.db import connection


class CreateRequestForm(forms.Form):
    sql = "SELECT branch_id,branch_name FROM branch;"
    cursor = connection.cursor()
    cursor.execute(sql)
    branchs = cursor.fetchall()

    license_plate = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '12EE345'}))
    from_branch = forms.CharField(label="From", widget=forms.Select(choices=branchs))
    to_branch = forms.CharField(label="To", widget=forms.Select(choices=branchs))
    reason = forms.CharField(widget=forms.Textarea(attrs={'name': 'body', 'rows': 2, 'cols': 2}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})


class VehicleRate(forms.Form):
    rates = [tuple([x, x]) for x in range(1, 6)]

    license_plate = forms.CharField(widget=forms.TextInput(attrs={'placeholder': '12EE345'}))
    comment = forms.CharField(widget=forms.Textarea(attrs={'name': 'body', 'rows': 2, 'cols': 2}))
    rate = forms.CharField(label="Rate", widget=forms.Select(choices=rates))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})


class MakeReservertion(forms.Form):
    sql = "SELECT insurance_price, insurance_type FROM insurance;"
    cursor = connection.cursor()
    cursor.execute(sql)
    insurances = cursor.fetchall()
    L2 = list(insurances)
    L2.append(['NULL', 'None'])
    T2 = tuple(L2)

    sql = "SELECT user_id, employee_name FROM chauffeur NATURAL JOIN (employee);"
    cursor.execute(sql)
    chauffeurs = cursor.fetchall()
    L1 = list(chauffeurs)
    L1.append(['NULL', 'None'])
    T1 = tuple(L1)

    reserver_id = forms.IntegerField(widget=forms.HiddenInput())
    daily_cost = forms.IntegerField(widget=forms.HiddenInput())

    start_date = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'DDDD/MM/YY'}))
    end_date = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'DDDD/MM/YY'}))
    reason = forms.CharField(widget=forms.Textarea(attrs={'name': 'body', 'rows': 2, 'cols': 2}))
    license_plate = forms.CharField(widget=forms.HiddenInput())

    chauffeur_id = forms.CharField(label="Pick your Chauffeurs", widget=forms.Select(choices=T1))
    insurance_type = forms.CharField(label="Pick your insurance", widget=forms.Select(choices=T2))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})


class CarPlate(forms.Form):
    plate = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
