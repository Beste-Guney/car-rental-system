from django.contrib.auth.views import LogoutView
from django.urls import path
from employee.views import *

app_name = 'employee'
urlpatterns = [
    path('employeeDashboard/<int:employee_id>', EmployeeMainPage.as_view(), name='employee-dashboard'),
    path('employeeReservations/', ReservationView.as_view(), name='view-reservations'),
    path('ajaxAcceptReservation/', accept_reservation, name='accept-reservation'),
    path('ajaxDeclineReservation/', decline_reservation, name='decline-reservation'),
    path('ajaxAcceptRequest/', accept_request, name='accept-request'),
    path('ajaxDeclineRequest/', decline_request, name='decline-request'),
    path('employeeRequests/', RequestsView.as_view(), name='view-requests'),
    path("logout/", LogoutView.as_view(), name="logout")
]