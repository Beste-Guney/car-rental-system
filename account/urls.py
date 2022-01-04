from django.urls import path
from account.views import RegisterManagerView, RegisterCustomer, LoginView, RegisterBranchEmployeeView, RegisterChaeffeurView, RegisterDamageExpert
from manager.views import *

urlpatterns = [
    path('signupCustomer/', RegisterCustomer.as_view(), name='customer_register'),
    path('signupBranchEmployee/', RegisterBranchEmployeeView.as_view(), name='branchemployee-register'),
    path('signupChaeffur/', RegisterChaeffeurView.as_view(), name='chauffeur-register'),
    path('signupDamageExpert/', RegisterDamageExpert.as_view(), name='damageexpert-register'),
    path('signupManager/', RegisterManagerView.as_view(), name='manager-register'),
    path('login/', LoginView.as_view(), name='login_user')
]
