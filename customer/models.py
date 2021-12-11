from django.shortcuts import render, redirect
from django.views import View
from django.db import connection
from django.views.generic.list import ListView
from django.http import JsonResponse
from manager.forms import BranchEmployeeCreationForm, ChauffeurCreationForm, DamageExpertCreationForm


def createModelBrandTable():
    cursor = connection.cursor()
    cursor.execute(
        'create table if not exists modelBrand(model varchar(15),brand varchar(20),primary key(model))engine=InnoDB;')

    return 'Model brand created'
