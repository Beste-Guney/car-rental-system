from django.shortcuts import render, redirect
from django.views import View
from django.db import connection
from .forms import CarPlate, MakeReservertion, VehicleRate, CreateRequestForm, BranchRate
from datetime import datetime


class RateBranch(View):

    def post(self, request):
        form = BranchRate(request.POST)

        if form.is_valid():
            customer_id = request.session['logged_in_user']
            branch_id = form.cleaned_data['branch']
            comment = form.cleaned_data['comment']
            score = form.cleaned_data['score']

            cursor = connection.cursor()
            sql = "INSERT INTO branch_rate (customer_id, branch_id, comment, score) VALUES ({}, {}, '{}', {});".format(
                customer_id, branch_id, comment, score)
            cursor.execute(sql)

            form = BranchRate()
            context = {
                'form': form,
                'message': 'Your evaluation is saved.'
            }
            return render(request, 'ratebranch.html', context)
        form = BranchRate()
        context = {
            'form': form,
            'message': 'Error occured. Try again later.'
        }
        return render(request, 'ratebranch.html', context)

    def get(self, request):
        form = BranchRate()
        context = {
            'form': form,
            'message': ''
        }
        return render(request, 'ratebranch.html', context)


class CreateRequest(View):

    def post(self, request):
        form = CreateRequestForm(request.POST)

        if form.is_valid():
            user_id = request.session['logged_in_user']
            license_plate = form.cleaned_data['license_plate']
            from_branch = form.cleaned_data['from_branch']
            to_branch = form.cleaned_data['to_branch']
            reason = form.cleaned_data['reason']
            cursor = connection.cursor()
            sql = "INSERT INTO request " \
                  "(req_id, made_by_customer, from_branch, to_branch, requested_vehicle, checked_by_employee, isApproved, reason) " \
                  "VALUES (NULL, {}, {}, {}, '{}', NULL, NULL, '{}');".format(user_id, from_branch, to_branch,
                                                                              license_plate, reason)
            cursor.execute(sql)
            cursor = connection.cursor()
            sql = "SELECT * FROM `reservation` WHERE reserver = {} and status = 'paid';".format(user_id)
            cursor.execute(sql)
            old_res = cursor.fetchall()
            form = CreateRequestForm()
            context = {
                'old_res': old_res,
                'form': form,
                'message': 'Request is taken.'
            }
            return render(request, 'customerRequest.html', context)

        cursor = connection.cursor()
        sql = "SELECT * FROM `reservation` WHERE reserver = {} and status = 'paid';".format(user_id)
        cursor.execute(sql)
        old_res = cursor.fetchall()
        form = CreateRequestForm()
        context = {
            'old_res': old_res,
            'form': form,
            'message': 'Error occured.'
        }
        return render(request, 'customerRequest.html', context)

    def get(self, request) -> 'html':
        user_id = request.session['logged_in_user']
        cursor = connection.cursor()
        sql = "SELECT * FROM `reservation` WHERE reserver = {} and status = 'paid';".format(user_id)
        cursor.execute(sql)
        old_res = cursor.fetchall()
        form = CreateRequestForm()
        context = {
            'old_res': old_res,
            'form': form,
            'message': ''
        }
        return render(request, 'customerRequest.html', context)


class RateCar(View):

    def post(self, request):
        form = VehicleRate(request.POST)

        if form.is_valid():
            license_plate = form.cleaned_data['license_plate']
            comment = form.cleaned_data['comment']
            rate = form.cleaned_data['rate']
            user_id = request.session['logged_in_user']
            cursor = connection.cursor()
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
