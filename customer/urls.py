from django.urls import path
from customer.views import customerRegisterPage

app_name = 'customer'
urlpatterns = [
    path('register/', customerRegisterPage.as_view(), name='customer_register'),
]
