from django.shortcuts import render
from django.views import View
from django.db import connection

# Create your views here.
class EmployeeMainPage(View):
    def get(self, request, employee_id):

        cursor = connection.cursor()
        cursor.execute(
            'select * from employee where user_id=\'' + str(employee_id) + '\''
        )
        result = cursor.fetchall()
        result = result[0]
        branch_id = result[3]
        employee_name = result[2]

        # finding the branch
        cursor.execute(
            'select * from branch where branch_id=\'' + str(branch_id) + '\''
        )
        result = cursor.fetchall()
        result = result[0]
        branch_name = result[2]

        return render(request, 'employeeDashboard.html',
                      {'branch_id': branch_id, 'branch_name': branch_name, 'name': employee_name})