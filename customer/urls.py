from django.urls import path
from customer.views import CustomerDashboard, MakeReservation, RateCar, CreateRequest, RateBranch, ReturnVehicle, \
    PayVehicle, ListReservations

app_name = 'customer'
urlpatterns = [
    path('customerDashboard/', CustomerDashboard.as_view(), name='customer_dashboard'),
    path('rateVehicle/', RateCar.as_view(), name='customer_rate_vehicle'),
    path('rateBranch/', RateBranch.as_view(), name='customer_rate_branch'),
    path('returnVehicle/', ReturnVehicle.as_view(), name='customer_return_vehicle'),
    path('createRequest/', CreateRequest.as_view(), name='customer_create_request'),
    path('makereservation/', MakeReservation.as_view(), name='customer_make_res'),
    path('payVehicle/<str:resno>', PayVehicle.as_view(), name='customer_pay_vehicle'),
    path('allReservations/', ListReservations.as_view(), name='reservation_list'),
    path('makereservation/<str:plate>', MakeReservation.as_view(), name='customer_make_res')
]
