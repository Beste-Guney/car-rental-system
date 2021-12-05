from django.urls import path
from account.views import RegisterCustomer, LoginView
from manager.views import ManagerMainPage

urlpatterns = [
    path('signupCustomer/', RegisterCustomer.as_view(), name='customer_register'),
    path('login/', LoginView.as_view(), name='login_user')
]