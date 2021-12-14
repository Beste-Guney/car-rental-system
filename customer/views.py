from django.shortcuts import render, redirect
from django.views import View
from django.db import connection
from .forms import CarPlate, MakeReservationForm, VehicleRate
from datetime import datetime

class RateCar(View):

    def post(self, request):
        form = VehicleRate(request.POST)

        if form.is_valid():
            license_plate = form.cleaned_data['license_plate']
            comment = form.cleaned_data['comment']
            rate = form.cleaned_data['rate']
            user_id = request.session['logged_in_user']
            cursor = connection.cursor()
            print(license_plate)
            print(rate)
            print(comment)
            print(user_id)
            sql = "INSERT INTO vehicle_rate (customer_id, license_plate, comment, score) " \
                  "VALUES ({}, '{}', '{}', {});".format(user_id, license_plate, comment, rate)
            cursor.execute(sql)

        return self.get(request)

    def get(self, request) -> 'html':
        user_id = request.session['logged_in_user']
        cursor = connection.cursor()
        sql = "SELECT * FROM `reservation` WHERE reserver = {} and status = 'paid';".format(user_id)
        cursor.execute(sql)
        old_res = cursor.fetchall()
        form = VehicleRate()
        context = {
            'old_res': old_res,
            'userid': user_id,
            'form': form
        }
        return render(request, 'ratevehicles.html', context)


class MakeReservation(View):

    def post(self, request):

        user_id = request.session['logged_in_user']
        form = MakeReservationForm(request.POST, user=user_id, license_plate=None, daily_cost=None)
        if form.is_valid():
            reserver_id = form.cleaned_data['reserver_id']
            reason = form.cleaned_data['reason']
            license_plate = form.cleaned_data['license_plate']
            daily_cost = form.cleaned_data['daily_cost']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            chauffeur_id = form.cleaned_data['chauffeur_id']
            insurance_type = form.cleaned_data['insurance_type']

            rental_period_in_days = abs((end_date - start_date).days);
            cost = rental_period_in_days * daily_cost

            cursor = connection.cursor()
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
                VALUES (NULL, '{}', '{}', 'not_accepted', '{}', '{}', NULL, '0', '{}', '{}', '{}', {}, NULL);
            """.format(start_date, end_date, cost, reserver_id, reason, insurance_type, license_plate,
                       chauffeur_id)
            cursor.execute(sql)

        return render(request, 'customerDashboard.html')

    def get(self, request, plate) -> 'html':
        cursor = connection.cursor()
        sql = "SELECT * FROM vehicle where license_plate = \'{}\';".format(plate)
        cursor.execute(sql)
        vehicle = cursor.fetchall()
        vehicleTuple = vehicle[0]

        user_id = request.session['logged_in_user']

        form = MakeReservationForm(user=user_id, license_plate=vehicleTuple[0], daily_cost=vehicleTuple[2])
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

class ListReservations(View):
    def get(self, request):
        reserver = request.session['logged_in_user']

        cursor = connection.cursor()
        cursor.execute(
            'SELECT * FROM reservation WHERE reserver =' + str(reserver) + ';'
        )
        result = cursor.fetchall()
        context ={
            'reservations': result
        }
        return render(request, 'listReservations.html', context)
