from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.db import connection
from pymysql import IntegrityError
import datetime
from .forms import CarPlate, MakeReservationForm, VehicleRate, CreateRequestForm, BranchRate, ReservationNo, Pay
from datetime import date


class PayVehicle(View):

    def post(self, request, resno):
        form = Pay(request.POST)

        if form.is_valid():
            branch_id = form.cleaned_data['branch']
            money = form.cleaned_data['money']
            plate = form.cleaned_data['plate']
            required_payment = form.cleaned_data['required_payment']
            res_no = form.cleaned_data['res_no']
            required_payment = float(required_payment)

            if required_payment != money:
                messages.error(request, 'Please enter correct amount.')
                return self.get(request, res_no)
            else:
                cursor = connection.cursor()
                sql = "UPDATE branch SET budget = budget + {} where branch_id = {};".format(money, branch_id)
                cursor.execute(sql)

                sql = "update vehicle set status = 'available', branch_id = {} where license_plate =  '{}';".format(
                    branch_id, plate)
                cursor.execute(sql)

                sql = "UPDATE reservation set status = 'paid' where reservation_number = {}".format(res_no)
                cursor.execute(sql)
                messages.success(request, 'Payment is taken. Thank you :)')
                return self.get(request, res_no)

        return redirect('/customer/error')

    def get(self, request, resno) -> 'html':
        user_id = request.session['logged_in_user']
        cursor = connection.cursor()
        sql = "SELECT discount_rate, user_id,customer_status FROM customer_discount NATURAL JOIN user WHERE user_id ={}".format(
            user_id)
        cursor.execute(sql)
        user_data = cursor.fetchall()
        discount_rate = user_data[0][0]

        sql = "SELECT reservation_number, license_plate, end_date, cost FROM reservation WHERE reservation_number = {}".format(
            resno)
        cursor.execute(sql)
        reservation = cursor.fetchall()

        res_no = reservation[0][0]
        license_plate = reservation[0][1]
        end_date = reservation[0][2]
        cost = reservation[0][3]

        today = date.today()
        fee_time = abs((today - end_date).days)

        if fee_time > 0:
            penalty = fee_time * 100
        else:
            penalty = 0
        total = cost + penalty

        discount = (total * int(discount_rate)) / 100

        form = Pay()
        context = {
            'res_no': res_no,
            'license_plate': license_plate,
            'discount_rate': discount_rate,
            'cost': cost,
            'penalty': penalty,
            'total': total,
            'discount': discount,
            'required_payment': total - discount,
            'form': form
        }
        return render(request, 'payVehicle.html', context)


class ReturnVehicle(View):

    def post(self, request):
        form = ReservationNo(request.POST)

        if form.is_valid():
            return redirect('customer:customer_pay_vehicle', resno=form.cleaned_data['ReservationNo'])

        return self.get(request)

    def get(self, request) -> 'html':
        user_id = request.session['logged_in_user']
        cursor = connection.cursor()
        sql = "SELECT reservation_number, license_plate, start_date,end_date,cost, status FROM `reservation` WHERE reserver = {} and status = 'accepted';".format(
            user_id)
        cursor.execute(sql)
        active_res = cursor.fetchall()

        sql = "SELECT discount_rate, user_id, customer_status FROM customer_discount NATURAL JOIN user WHERE user_id ={}".format(
            user_id)
        cursor.execute(sql)
        user_data = cursor.fetchall()

        discount_rate = user_data[0][0]
        user_status = user_data[0][2]

        form = ReservationNo()
        context = {
            'old_res': active_res,
            'form': form,
            'discount_rate': discount_rate,
            'user_status': user_status
        }
        return render(request, 'returnvehicles.html', context)


class RateBranch(View):

    def post(self, request):
        form = BranchRate(request.POST)

        if form.is_valid():
            customer_id = request.session['logged_in_user']
            branch_id = form.cleaned_data['branch']
            comment = form.cleaned_data['comment']
            score = form.cleaned_data['score']

            try:
                print("asdjkgnkjadfnhkadf")
                cursor = connection.cursor()
                sql = "INSERT INTO branch_rate (customer_id, branch_id, comment, score) VALUES ({}, {}, '{}', {});".format(
                    customer_id, branch_id, comment, score)
                cursor.execute(sql)
            except:
                messages.error(request, 'You already evaluated this branch.')
                return self.get(request)

            messages.success(request, 'You evaluation is saved.')
            return self.get(request)

        return redirect('/customer/error')

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
        user_id = request.session['logged_in_user']
        if form.is_valid():
            user_id = request.session['logged_in_user']
            license_plate = form.cleaned_data['license_plate']
            to_branch = form.cleaned_data['to_branch']
            reason = form.cleaned_data['reason']
            cursor = connection.cursor()

            sql = """SELECT branch_id FROM vehicle WHERE license_plate = "{}";""".format(license_plate)
            cursor.execute(sql)
            from_branch = cursor.fetchall()
            sql = "INSERT INTO request " \
                  "(req_id, made_by_customer, from_branch, to_branch, requested_vehicle, checked_by_employee, isApproved, reason) " \
                  "VALUES (NULL, {}, {}, {}, '{}', NULL, NULL, '{}');".format(user_id, from_branch[0][0], to_branch,
                                                                              license_plate, reason)
            cursor.execute(sql)
            sql = "SELECT * FROM request, (SELECT branch_id, branch_name FROM branch) AS from_branch_name, (SELECT branch_id, branch_name FROM branch) AS to_branch_name WHERE from_branch = from_branch_name.branch_id and to_branch = to_branch_name.branch_id and made_by_customer = {};".format(user_id)
            cursor.execute(sql)
            old_req = cursor.fetchall()
            form = CreateRequestForm()
            context = {
                'old_req': old_req,
                'form': form,
                'message': 'Request is taken.',
            }
            return render(request, 'customerRequest.html', context)

        cursor = connection.cursor()
        sql = "SELECT * FROM request, (SELECT branch_id, branch_name FROM branch) AS from_branch_name, (SELECT branch_id, branch_name FROM branch) AS to_branch_name WHERE from_branch = from_branch_name.branch_id and to_branch = to_branch_name.branch_id and made_by_customer = {};".format(user_id)
        cursor.execute(sql)
        old_req = cursor.fetchall()
        form = CreateRequestForm()
        context = {
            'old_req': old_req,
            'form': form,
            'message': 'Error occured.'
        }
        return render(request, 'customerRequest.html', context)

    def get(self, request) -> 'html':
        user_id = request.session['logged_in_user']
        cursor = connection.cursor()
        sql = "SELECT * FROM request, (SELECT branch_id, branch_name FROM branch) AS from_branch_name, (SELECT branch_id, branch_name FROM branch) AS to_branch_name WHERE from_branch = from_branch_name.branch_id and to_branch = to_branch_name.branch_id and made_by_customer = {};".format(user_id)
        cursor.execute(sql)
        old_req = cursor.fetchall()
        form = CreateRequestForm()
        context = {
            'old_req': old_req,
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
            try:
                sql = "INSERT INTO vehicle_rate (customer_id, license_plate, comment, score) " \
                      "VALUES ({}, '{}', '{}', {});".format(user_id, license_plate, comment, rate)
                cursor.execute(sql)
            except:
                messages.error(request, 'You already evaluated this vehicle.')
                return self.get(request)

            messages.success(request, 'Your evaluation is saved.')
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
        error_message = ''

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
            if start_date > end_date: 
                return redirect('/customer/errorDate')

            rental_period_in_days = abs((end_date - start_date).days);
            cost = rental_period_in_days * daily_cost

            cursor = connection.cursor()
            print(insurance_type != 'NULL')
            if insurance_type != 'NULL':
                sql = "SELECT insurance_type FROM `insurance` WHERE insurance_price = {};".format(insurance_type)
                cursor.execute(sql)
                insurances = cursor.fetchall()
                insurance_type = insurances[0][0]

            # some assertions are needed before inserting a new reservation


            # assertion 1- if the car to be reserved is not available
            #assertion_1_sql = "create assertion vehicle_availability_constraint check (unique (select * from reservation R where R.license_plate = " + str(license_plate) + " and DATEPART(year, end_date) = " + str(actual_end.year) + " and  DATEPART(month, start_date) between " + str(actual_start.month) + " and " + str(actual_end.month) + " and DATEPART(day, start_date) between " + str(actual_start.day) +  " and " +  str(actual_end.day) + " DATEPART(day, end_date)"
            # cursor.execute('select start_date, end_date from reservation where license_plate  = ' + str(license_plate) + ';')
            # result = cursor.fetchall()
            # for res in result:
            #     start = res[0]
            #     end = res[1]
            #
            #     if not (start_date)


            #assertion 2- if you already have an reservation that day
            #cursor.execute('select * from reservation  where reserver = ' + str(user_id) + ' and DATEPART(year, end_date) = ' + str(actual_end.year) + ' and DATEPART(year, end_date)')

            #cursor.execute()



            #assertion 3- if the user has not paid for a reservation before
            assertion_3_sql = " select * from reservation where reserver = " + str(user_id) + " and status = \'not_paid\'"
            cursor.execute(assertion_3_sql)
            result = cursor.fetchall()
            if len(result) != 0:
                print('hfjdfhdjfj')
                error_message = 'First pay your previous reservations'
                return render(request, 'error.html', {'message': error_message})

            #assertion 4- if user driving license info doesnt allow it to rent this car
            assertion_4_sql = "select car_type from vehicle natural join car where license_plate = \'" + str(license_plate) + '\';'
            cursor.execute(assertion_4_sql)
            result_car_type = cursor.fetchall()
            result_car_type = result_car_type[0]

            cursor.execute('select license_type from driving_license where user_id = \'' + str(user_id) + '\';')
            result_user_license = cursor.fetchall()
            result_user_license = result_user_license[0]
            if result_user_license[0][0:1] != result_car_type[0] and chauffeur_id == 'NULL':
                error_message = 'You cannot drive this car, you need a chaeffuer'
                return render(request, 'error.html', {'message': error_message})


            sql = """
            INSERT INTO `reservation` 
            (`start_date`, `end_date`, `status`, `cost`, `reserver`, 
            `checked_by`, `isApproved`, `reason`, `insurance_type`, `license_plate`, `reserved_chauf_id`, `isChaufAccepted`) 
            VALUES ('{}', '{}', 'not_accepted', '{}', '{}', NULL, 'false', '{}', '{}', '{}', {}, NULL);
        """.format(start_date, end_date, cost, reserver_id, reason, insurance_type, license_plate,
                   chauffeur_id)

            print(sql)
            cursor.execute(sql)

            return redirect('/customer/reservationsuccess')

        return render(request, 'error.html', {'message': error_message})

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
            'SELECT * FROM vehicle NATURAL JOIN branch WHERE status = \'available\';'
        )
        desc = cursor.fetchall()
        context = {
            'vehicles': desc,
        }
        return render(request, 'customerDashboard.html', context)


class Error(View):

    def get(self, request):
        return render(request, 'error.html')

class DateError(View):
    def get(self, request):
        return render(request, 'errorDate.html')

class ReservationComplate(View):
    def get(self, request):
        return render(request, 'reservationcomplate.html')


class ListReservations(View):
    def get(self, request):
        reserver = request.session['logged_in_user']

        cursor = connection.cursor()
        cursor.execute(
            'SELECT * FROM reservation WHERE reserver =' + str(reserver) + ';'
        )
        result = cursor.fetchall()
        context = {
            'reservations': result
        }
        return render(request, 'listReservations.html', context)

class OrderReservations(View):
    def post(self, request):
        order = request.POST['order-by']
        reserver = request.session['logged_in_user']
        cursor = connection.cursor()

        if int(order) == 1:
            cursor.execute(
                'SELECT * FROM reservation WHERE reserver =' + str(reserver) + ' order by start_date;'
            )
        elif int(order) == 2:
            cursor.execute(
                'SELECT * FROM reservation WHERE reserver =' + str(reserver) + ' order by cost;'
            )
        else:
            cursor.execute(
                'SELECT * FROM reservation WHERE reserver =' + str(reserver) + ' order by end_date;'
            )
        result = cursor.fetchall()
        context = {
            'reservations': result
        }
        return render(request, 'listReservations.html', context)