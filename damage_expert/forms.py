from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.shortcuts import render, redirect
from django.views import View
from django.db import connection

class ReservationCheck(forms.Form):
    reservationNo = forms.CharField(widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ReviewReservationForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea(attrs={'name': 'body', 'rows': 8, 'cols': 8}))
    reservationNo = forms.CharField(widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        reservationNo = kwargs.pop('resNo')
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': "form-group form-control mt-3"})
        self.fields['reservationNo'].widget.attrs.update({'value': reservationNo})

class VehicleCheck(forms.Form):
    lilcensePlate = forms.CharField(widget=forms.HiddenInput())
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)