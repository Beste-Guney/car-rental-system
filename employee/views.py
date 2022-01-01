from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.db import connection


# Create your views here.
#method to get emplyee info and branch info
def getInfo(self, request):
    user_id = request.session['logged_in_user']
    cursor = connection.cursor()
    cursor.execute(
        'select * from employee where user_id=\'' + str(user_id) + '\''
    )
    result = cursor.fetchall()
    result = result[0]
    branch_id = result[3]
    employee_name = result[2]

    cursor = connection.cursor()
    cursor.execute(
        'select * from branch where branch_id=\'' + str(branch_id) + '\''
    )
    result = cursor.fetchall()
    result = result[0]
    branch_name = result[2]

    return branch_id, employee_name, branch_name


class EmployeeMainPage(View):
    def get(self, request, employee_id):

        branch_id, employee_name, branch_name = getInfo(self, request)
        return render(request, 'employeeReservation.html',
                      {'branch_id': branch_id, 'branch_name': branch_name, 'name': employee_name})


class ReservationView(View):
    def get(self, request):
        branch_id, employee_name, branch_name = getInfo(self, request)

        #getting reservations
        cursor = connection.cursor()
        cursor.execute(
            'select reservation.reservation_number, reservation.start_date, reservation.end_date, reservation.license_plate, '
            'reservation.status, reservation.cost, customer.customer_name, reservation.insurance_type, reservation.reserved_chauf_id from reservation,vehicle, user, customer where reservation.license_plate = vehicle.license_plate and '
            'reservation.reserver= user.user_id and user.user_id = customer.user_id and vehicle.branch_id= ' + str(branch_id) + ';'
        )
        result = cursor.fetchall()

        #getting reserver info with join

        context = {
            'branch_name': branch_name,
            'reservations': result,
            'branch_id': branch_id
        }
        return render(request, 'employeeReservation.html', context)

class RequestsView(View):
    def get(self, request):
        branch_id, employee_name, branch_name = getInfo(self, request)
        user_id = request.session['logged_in_user']
        #getting reservations
        cursor = connection.cursor()
        cursor.execute(
            'select customer.customer_name, B1.branch_name, B2.branch_name, request.requested_vehicle, request.reason, request.req_id, request.isApproved, request.to_branch '
            #'from request where request.checked_by_employee = ' + str(user_id) + ';'
            'from request, customer, branch B1, branch B2 where request.made_by_customer = customer.user_id and '
            'B1.branch_id = request.from_branch and B2.branch_id = request.to_branch;'
        )
        result = cursor.fetchall()
        for res in result:
            print(res)

        context = {
            'branch_name': branch_name,
            'requests': result,
            'branch_id': branch_id
        }
        #getting reserver info with join
        return render(request, 'employeeRequests.html', context)


def accept_reservation(request):
    print('here')
    employee_id = request.GET.get('employee_id', None)
    reservation_id = request.GET.get('reservation_id', None)

    #changing the status of reservation
    cursor = connection.cursor()
    cursor.execute('update reservation set status = \'accepted\'  where reservation_number = \'' + str(reservation_id) + '\';')
    cursor.execute('update reservation set checked_by = ' + employee_id +'  where reservation_number = \'' + str(reservation_id) + '\';')
    data = {}
    return JsonResponse(data)

def decline_reservation(request):
    print('here')
    employee_id = request.GET.get('employee_id', None)
    reservation_id = request.GET.get('reservation_id', None)

    # changing the status of reservation
    cursor = connection.cursor()
    cursor.execute(
        'update reservation set status = \'canceled\'  where reservation_number = \'' + str(reservation_id) + '\';')
    cursor.execute('update reservation set checked_by = ' + employee_id +'  where reservation_number = \'' + str(reservation_id) + '\';')
    data = {}
    return JsonResponse(data)

def accept_request(request):
    print('here')
    employee_id = request.GET.get('employee_id', None)
    request_id = request.GET.get('req_id', None)

    #changing the status of request
    cursor = connection.cursor()
    cursor.execute('select requested_vehicle, to_branch from request where req_id = \'' + str(request_id) + '\';')
    result = cursor.fetchall()
    for res in result:
            print(res)

    cursor.execute('update request set isApproved = 1  where req_id = \'' + str(request_id) + '\';')
    cursor.execute('update request set checked_by_employee = ' + str(employee_id) + '  where req_id = \'' + str(request_id) + '\';')
    cursor.execute('update vehicle set branch_id = ' + str(result[0][1]) + '  where license_plate = \'' + str(result[0][0]) + '\';')

    data = {}
    return JsonResponse(data)

def decline_request(request):
    print('here')
    employee_id = request.GET.get('employee_id', None)
    request_id = request.GET.get('req_id', None)


    #changing the status of request
    cursor = connection.cursor()
    cursor.execute('update request set isApproved = 0  where req_id = \'' + str(request_id) + '\';')
    cursor.execute('update request set checked_by_employee = ' + str(employee_id) + '  where req_id = \'' + str(request_id) + '\';')
    data = {}
    return JsonResponse(data)

class BranchCarView(View):

    def get(self, request, branch_id):
        cursor = connection.cursor()
        cursor.execute(
            'select * from vehicle where branch_id=\'' + str(branch_id) + '\''
        )
        result = cursor.fetchall()

        # storing vehicle info in arrays
        vehicle_info = []

        for car in result:
            item_detail = [car[0], car[1], car[2], car[3], car[4], car[5], car[6], car[7]]
            vehicle_info.append(item_detail)

        cursor.execute(
            'select branch_name from branch where branch_id=\'' + str(branch_id) + '\''
        )
        result = cursor.fetchall()
        result = result[0]
        branch_name = result[0]

        models, brands = models_and_brands()

        return render(request, 'branchCarsEmployee.html',
                      {'vehicles': vehicle_info, 'branch_name': branch_name, 'branch_id': branch_id, 'models': models,
                       'brands': brands})

def models_and_brands():
    # sending existing models from db to view
    cursor = connection.cursor()
    cursor.execute(
        'select * from model_brand;'
    )
    result = cursor.fetchall()
    models = []

    for res in result:
        models.append(res[0])

    #sending existng brands
    brands = set()

    for res in result:
        brands.add(res[1])

    return models, brands


class FilterReservations(View):
    def post(self, request):
        branch_id, employee_name, branch_name = getInfo(self, request)
        customer_name = request.POST['customer_name']
        status = request.POST['reservation-status']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        customer_name = customer_name.lower()
        cursor = connection.cursor()

        # getting reservations
        if customer_name:
            cursor.execute(
                'create view filter1 as (select reservation.reservation_number, reservation.start_date as start_date, reservation.end_date as end_date, reservation.license_plate, '
                'reservation.status as status, reservation.cost, customer.customer_name, reservation.insurance_type, reservation.reserved_chauf_id from reservation,vehicle, user, customer where reservation.license_plate = vehicle.license_plate and '
                'reservation.reserver= user.user_id and user.user_id = customer.user_id and vehicle.branch_id= ' + str(
                    branch_id) + ' and customer.customer_name like \'' + customer_name + '%\');'
            )
        else:
            cursor.execute(
                'create view filter1 as (select reservation.reservation_number, reservation.start_date as start_date, reservation.end_date as end_date, reservation.license_plate, '
                'reservation.status as status, reservation.cost, customer.customer_name, reservation.insurance_type, reservation.reserved_chauf_id from reservation,vehicle, user, customer where reservation.license_plate = vehicle.license_plate and '
                'reservation.reserver= user.user_id and user.user_id = customer.user_id and vehicle.branch_id= ' + str(
                    branch_id) + ' );'
            )

        if status != 'empty':
            cursor.execute('create view filter2 as select * from filter1 where status = \'' + str(status) + '\';')
        else:
            cursor.execute('create view filter2 as select * from filter1')

        if start_date:
            cursor.execute('create view filter3 as (select * from filter2 where start_date <= \'' + start_date + '\' and end_date >= \'' + start_date + '\');')
        else:
            cursor.execute('create view filter3 as (select * from filter2);')

        if end_date:
            cursor.execute('create view filter4 as (select * from filter3 where end_date <= \'' + end_date + '\' and start_date <= \'' + end_date + '\');')
        else:
            cursor.execute('create view filter4 as (select * from filter3);')

        cursor.execute('select * from filter4 ')
        result = cursor.fetchall()

        cursor.execute('drop view filter1')
        cursor.execute('drop view filter2')
        cursor.execute('drop view filter3')
        cursor.execute('drop view filter4')

        context = {
            'branch_name': branch_name,
            'reservations': result,
            'branch_id': branch_id
        }
        return render(request, 'employeeReservation.html', context)

class FilterVehicles(View):
    def post(self, request):
        branch_id, employee_name, branch_name = getInfo(self, request)
        cursor = connection.cursor()

        # taking filtering conditions from post
        license = request.POST['license']
        age = request.POST['age-vehicle']
        model = request.POST['model-vehicle']
        kilometers = request.POST['kilometers']
        brand = request.POST['brand']
        low = request.POST['lowest']
        high = request.POST['highest']

        # if plate is entered find the car
        if license:
            cursor.execute(
                'create view filter6 as select * from vehicle where license_plate like \'' + license + '%\';'
            )
        else:
            cursor.execute(
                'create view filter6 as select * from vehicle ;'
            )
        # filtering according to other conditions
        if int(age) != -1:
            print('here1')
            upper_bound = int(age) + 5
            cursor.execute(
                'create view filter1 as select * from filter6 where age between\'' + str(age) + '\'and \'' + str(
                    upper_bound) + '\';'
            )

        else:
            cursor.execute(
                'create view filter1 as '
                'select * from filter6;'
            )

        if model != 'empty':
            cursor.execute(
                'create view filter2 as select * from filter1 where model=\'' + model + '\';'
            )
        else:
            cursor.execute(
                'create view filter2 as '
                'select * from filter1;'
            )

        if int(kilometers) != -1:
            print('here3')

            if int(kilometers) == 40000:
                cursor.execute(
                    'create view filter3 as '
                    'select * from filter2 where kilometers > 40000;'
                )
            else:
                upper_bound = int(kilometers) * 2
                cursor.execute(
                    'create view filter3 as select * from filter2 where kilometers between ' + str(
                        kilometers) + ' and ' + str(upper_bound) + ';'
                )


        else:
            cursor.execute(
                'create view filter3 as '
                'select * from filter2;'
            )

        if int(high) == 0:
            cursor.execute(
                'create view filter4 as select * from filter3 where daily_rent_price > ' + str(low) + ';'
            )
        else:
            cursor.execute(
                'create view filter4 as select * from filter3 where daily_rent_price between ' + str(
                    low) + ' and ' + str(high) + ';'
            )

        if brand != 'empty':
            cursor.execute(
                'create view filter5 as select * from filter4 where brand=\'' + brand + '\';'
            )
        else:
            cursor.execute(
                'create view filter5 as select * from filter4;'
            )

        # gathering filtered vehicles
        cursor.execute(
            'select * from vehicle, filter5 where vehicle.license_plate = filter5.license_plate and vehicle.branch_id = ' + str(branch_id) + ';'
        )
        result = cursor.fetchall()
        vehicle_info = []

        for car in result:
            item_detail = [car[0], car[1], car[2], car[3], car[4], car[5], car[6]]
            vehicle_info.append(item_detail)

        cursor.execute('drop view filter1')
        cursor.execute('drop view filter2')
        cursor.execute('drop view filter3')
        cursor.execute('drop view filter4')
        cursor.execute('drop view filter5')
        cursor.execute('drop view filter6')
        models, brands = models_and_brands()

        return render(request, 'branchCarsEmployee.html',
                      {'vehicles': vehicle_info, 'branch_name': branch_name, 'branch_id': branch_id, 'models': models,
                       'brands': brands})
