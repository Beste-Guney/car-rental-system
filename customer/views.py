from django.shortcuts import render, redirect
from django.views import View
from django.db import connection
from django.views.generic.list import ListView
from django.http import JsonResponse
from manager.forms import BranchEmployeeCreationForm, ChauffeurCreationForm, DamageExpertCreationForm


class customerRegisterPage(View):

    def get(self, request) -> 'html':
        return render(request, 'register.html')
