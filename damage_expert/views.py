from django.shortcuts import redirect, render
from django.views import View
from django.db import connection
from django.http import JsonResponse

from damage_expert.forms import *

# Create your views here.

def getExpertInfo(self, request):
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

class DamageExpertDashboard(View):
    def get(self, request, expert_id):
        user_id = request.session['logged_in_user']
        sql = "SELECT * FROM rental2.reservation WHERE status = 'paid' and current_timestamp() > end_date and reservation_number not in (SELECT issued_reservation FROM damage_report);"
        cursor = connection.cursor()
        cursor.execute(sql)
        paid_res = cursor.fetchall()
        context = {
            'user_id' : user_id,
            'paid_res' : paid_res
        }
        return render(request, 'damageExpertiseDashboard.html', context)
    def post(self, request, expert_id):
        user_id = request.session['logged_in_user']
        form = ReservationCheck(request.POST)
        if form.is_valid():
            return redirect('damage_expert:damage-expert-review', res_no = form.cleaned_data['reservationNo'])
        print("DAMAGESOSSOROSEIRSIN")
        sql = "SELECT * FROM rental2.reservation WHERE status = 'paid' and current_timestamp() > end_date and reservation_number not in (SELECT issued_reservation FROM damage_report); ;"
        cursor = connection.cursor()
        cursor.execute(sql)
        paid_res = cursor.fetchall()
        context = {
            'user_id' : user_id,
            'paid_res' : paid_res
        }
        return render(request, 'damageExpertiseDashboard.html', context)


class ReviewReservation(View):
    def get(self, request, res_no):
        user_id = request.session['logged_in_user']
        form = ReviewReservationForm(resNo = res_no)
        context = {
            'form' : form,
            'user_id' : user_id,
            'message' : ''
        }
        return render(request, 'damageExpertiseReview.html', context)
    def post(self, request):
        form = ReviewReservationForm(request.POST, resNo = None)
        if form.is_valid():
            user_id = request.session['logged_in_user']
            reason = form.cleaned_data['reason']
            resNo = form.cleaned_data['reservationNo']
            sql = "SELECT cost FROM reservation WHERE reservation_number = {};".format(resNo)
            cursor = connection.cursor()
            cursor.execute(sql)
            cost = cursor.fetchall()
            print("cost = ", cost[0][0])
            sql = "INSERT INTO damage_report (issue_id, description, type, cost, author_expertise_id, issued_reservation) VALUES (NULL, '{}', NULL, {}, {}, {});".format(reason, cost[0][0], user_id, resNo)
            cursor = connection.cursor()
            cursor.execute(sql)
            context = {
                'form' : form,
                'user_id' : user_id,
                'message' : 'Review successful'
            }
            return render(request, 'damageExpertiseReview.html', context)
        user_id = request.session['logged_in_user']
        sql = "SELECT * FROM rental2.reservation WHERE status = 'paid' and current_timestamp() > end_date;"
        cursor = connection.cursor()
        cursor.execute(sql)
        paid_res = cursor.fetchall()
        context = {
            'paid_res' : paid_res
        }
        return redirect('damage_expert:damage-expert-dashboard', expert_id = user_id)

class CheckAssigned(View):
    def get(self, request, expert_id):
        user_id = request.session['logged_in_user']
        sql = "SELECT * FROM assign_check WHERE assigned_expertise_id = {};".format(user_id)
        cursor = connection.cursor()
        cursor.execute(sql)
        assigned = cursor.fetchall()
        context = {
            'user_id' : user_id,
            'assigned' : assigned
        }
        return render(request, 'damageExpertiseAssignCheck.html', context)
    def post(self, request, expert_id):
        user_id = request.session['logged_in_user']
        l1 = request.POST.get("licensePlate","")
        sql = "DELETE FROM assign_check WHERE assigned_expertise_id = {} and assigned_vehicle_license_plate = '{}';".format(user_id, l1)
        cursor = connection.cursor()
        cursor.execute(sql)
        sql = "SELECT * FROM assign_check WHERE assigned_expertise_id = {};".format(user_id)
        cursor = connection.cursor()
        cursor.execute(sql)
        assigned = cursor.fetchall()
        context = {
            'user_id' : user_id,
            'assigned' : assigned
        }
        return render(request, 'damageExpertiseAssignCheck.html', context)
