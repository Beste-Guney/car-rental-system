from django.shortcuts import render, redirect
from django.views import View
from django.db import connection
from .forms import CarPlate, MakeReservertion
from datetime import datetime
from django.views.generic.list import ListView
from django.http import JsonResponse


class MakeReservation(View):

    def post(self, request):
        form = MakeReservertion(request.POST)
        if form.is_valid():
            reserver_id = form.cleaned_data['reserver_id']
            reason = form.cleaned_data['reason']
            license_plate = form.cleaned_data['license_plate']
            daily_cost = form.cleaned_data['daily_cost']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            chauffeur_id = form.cleaned_data['chauffeur_id']
            insurance_type = form.cleaned_data['insurance_type']

            start_date_obj = datetime.strptime(start_date, '%Y/%m/%d')
            end_date_obj = datetime.strptime(end_date, '%Y/%m/%d')

            rental_period_in_days = abs((end_date_obj - start_date_obj).days);
            cost = rental_period_in_days * daily_cost

            cursor = connection.cursor()
            print(insurance_type)
            print(insurance_type != 'NULL')
            if insurance_type != 'NULL':
                sql = "SELECT insurance_type FROM `insurance` WHERE insurance_price = {};".format(insurance_type)
                cursor.execute(sql)
                insurances = cursor.fetchall()
                insurance_type = insurances[0][0]

            sql = """
                INSERT INTO `reservation` 
                (`reservation_number`, `start_date`, `end_date`, `status`, `cost`, `reserver`, 
                `checked_by`, `isApproved`, `reason`, `insurance_type`, `license_plate`, `reserved_chauf_id`, `isChaufAccepted`) 
                VALUES (NULL, '{}', '{}', 'not_paid', '{}', '{}', NULL, '0', '{}', '{}', '{}', {}, NULL);
            """.format(start_date, end_date, cost, reserver_id, reason, insurance_type, license_plate,
                       chauffeur_id)
            cursor.execute(sql)

        return render(request, 'customerDashboard.html')

    def get(self, request, plate) -> 'html':
        cursor = connection.cursor()
        sql = "SELECT * FROM vehicle where license_plate = \'{}\';".format(plate)
        cursor.execute(sql)
        vehicle = cursor.fetchall()

        form = MakeReservertion()
        context = {
            'vehicle': vehicle[0],
            'userid': request.session['logged_in_user'],
            'form': form
        }
        return render(request, 'makeReservation.html', context)


class CustomerDashboard(View):

    def post(self, request):
        form = CarPlate(request.POST)

        if form.is_valid():
            return redirect('customer:customer_make_res', plate=form.cleaned_data['plate'])

        return render(request, 'customerDashboard.html')

    def get(self, request) -> 'html':
        cursor = connection.cursor()
        cursor.execute(
            'SELECT * FROM vehicle WHERE status = \'available\';'
        )
        desc = cursor.fetchall()
        context = {
            'vehicles': desc,
        }
        return render(request, 'customerDashboard.html', context)
