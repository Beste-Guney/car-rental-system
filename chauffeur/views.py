from django.contrib import messages
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views import View
from django.db import connection

class ChauffeurDashboard(View):
    def get(self, request):
        chauffeur_id = request.session['logged_in_user']
        cursor = connection.cursor()
        cursor.execute(
            'SELECT R.reservation_number, R.start_date, R.end_date, R.status, C.customer_name, E.employee_name, R.license_plate, R.isChaufAccepted FROM reservation R, employee E, customer C WHERE R.reserved_chauf_id = ' + str(chauffeur_id) + 
            ' and C.user_id = R.reserver and E.user_id = R.checked_by and R.status = \'accepted\';'
        )
        desc = cursor.fetchall()
        context = {
            'chauffeur_requests': desc,
        }
        return render(request, 'chauffeurDashboard.html', context)

def accept_request(request):
    reservation_id = request.GET.get('reservation_id', None)

    #changing the status of reservation
    cursor = connection.cursor()
    cursor.execute('update reservation set isChaufAccepted = 1  where reservation_number = \'' + str(reservation_id) + '\';')

    data = {}
    return JsonResponse(data)

def decline_request(request):
    reservation_id = request.GET.get('reservation_id', None)

    #changing the status of reservation
    cursor = connection.cursor()
    cursor.execute('update reservation set isChaufAccepted = 0  where reservation_number = \'' + str(reservation_id) + '\';')

    data = {}
    return JsonResponse(data)