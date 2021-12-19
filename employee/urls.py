from django.urls import path
from employee.views import *

app_name = 'employee'
urlpatterns = [
    path('employeeDashboard/<int:employee_id>', EmployeeMainPage.as_view(), name='employee-dashboard'),

]