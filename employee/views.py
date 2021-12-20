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
        return render(request, 'employeeDashboard.html',
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
        for res in result:
            print(res)

        #getting reserver info with join

        context = {
            'branch_name': branch_name,
            'reservations': result
        }
        return render(request, 'employeeReservation.html', context)


def accept_reservation(request):
    print('here')
    employee_id = request.GET.get('employee_id', None)
    reservation_id = request.GET.get('reservation_id', None)

    #changing the status of reservation
    cursor = connection.cursor()
    cursor.execute('update reservation set status = \'accepted\'  where reservation_number = \'' + str(reservation_id) + '\';')
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
    data = {}
    return JsonResponse(data)

