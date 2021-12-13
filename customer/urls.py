from django.urls import path
from customer.views import CustomerDashboard, MakeReservation, RateCar, CreateRequest, RateBranch

app_name = 'customer'
urlpatterns = [
    path('customerDashboard/', CustomerDashboard.as_view(), name='customer_dashboard'),
    path('rateVehicle/', RateCar.as_view(), name='customer_rate_vehicle'),
    path('rateBranch/', RateBranch.as_view(), name='customer_rate_branch'),
    path('createRequest/', CreateRequest.as_view(), name='customer_create_request'),
    path('makereservation/', MakeReservation.as_view(), name='customer_make_res'),
    path('makereservation/<str:plate>', MakeReservation.as_view(), name='customer_make_res')
]
