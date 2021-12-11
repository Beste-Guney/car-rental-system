from django.shortcuts import render, redirect
from django.views import View
from django.db import connection
from django.views.generic.list import ListView
from django.http import JsonResponse
from manager.forms import BranchEmployeeCreationForm, ChauffeurCreationForm, DamageExpertCreationForm


class customerDashboard(View):

    def get(self, request) -> 'html':
        cursor = connection.cursor()
        cursor.execute(
            'SELECT * FROM vehicle WHERE status = \'available\';'
        )
        desc = cursor.fetchall()
        print(desc)
        context = {
            'vehicals': desc,
            'name': 'kaan'
        }
        return render(request, 'customerDashboard.html', context)
