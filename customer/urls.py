from django.urls import path
from customer.views import PenaltiesView, cancelReservation, OrderReservations, CustomerDashboard, MakeReservation, RateCar, CreateRequest, RateBranch, ReturnVehicle, PayVehicle, ListReservations, ReservationComplate, Error, DateError

from django.contrib.auth.views import LogoutView



app_name = 'customer'
urlpatterns = [
    path('customerDashboard/', CustomerDashboard.as_view(), name='customer_dashboard'),
    path('penalties/', PenaltiesView.as_view(), name='customer-penalties'),
    path('rateVehicle/', RateCar.as_view(), name='customer_rate_vehicle'),
    path('rateBranch/', RateBranch.as_view(), name='customer_rate_branch'),
    path('error/', Error.as_view(), name='customer_error'),
    path('errorDate', DateError.as_view(), name='customer_date_error'),
    path('reservationsuccess/', ReservationComplate.as_view(), name='customer_reservation_complate'),
    path('returnVehicle/', ReturnVehicle.as_view(), name='customer_return_vehicle'),
    path('createRequest/', CreateRequest.as_view(), name='customer_create_request'),
    path('makereservation/', MakeReservation.as_view(), name='customer_make_res'),
    path('payVehicle/<str:resno>', PayVehicle.as_view(), name='customer_pay_vehicle'),
    path('allReservations/', ListReservations.as_view(), name='reservation_list'),
    path('makereservation/<str:plate>', MakeReservation.as_view(), name='customer_make_res'),
    path('orderReservations/', OrderReservations.as_view(), name='order_reservations'),
    path('ajax/cancelReservation/', cancelReservation, name='ajax_cancel_reservation'),
    path("logout/", LogoutView.as_view(), name="logout")
]
