from django.urls import path
from customer.views import customerDashboard

app_name = 'customer'
urlpatterns = [
    path('customerDashboard/', customerDashboard.as_view(), name='customer_register'),
]
