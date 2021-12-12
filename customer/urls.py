from django.urls import path
from customer.views import CustomerDashboard, MakeReservation

app_name = 'customer'
urlpatterns = [
    path('customerDashboard/', CustomerDashboard.as_view(), name='customer_dashboard'),
    path('makereservation/<str:plate>', MakeReservation.as_view(), name='customer_make_res'),
    path('makereservation/', MakeReservation.as_view(), name='customer_make_res')
]
