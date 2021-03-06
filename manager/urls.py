from django.contrib.auth.views import LogoutView
from django.urls import path
from manager.views import *

app_name = 'manager'
urlpatterns = [
    path('managerDashboard/<int:manager_id>', StatisticsView.as_view(), name='manager_dashboard'),
    path('branchCars/<int:branch_id>', BranchCarView.as_view(), name='cars_at_branch'),
    path('buyCar/<int:branch_id>', BuyCarView.as_view(), name='buy-available-cars'),
    path('assignEmployee/', AssignVehicleCheck.as_view(), name='manager-assign-vehicle'),
    path('ajax/buyCar', ajaxBuyCar, name='ajax_buy_car'),
    path('ajax/fireEmployee', ajaxFireEmployee, name='ajax_fire_employee'),
    path('employeeList/<int:branch_id>', EmployeeView.as_view(), name='branch-employees'),
    path('addBranchEmployee/', AddBranchEmployeeView.as_view(), name='add-branch-employee'),
    path('addChauffeur/', AddChauffeurView.as_view(), name='add-chauffeur'),
    path('addDamageExpert/', AddDamageExpertView.as_view(), name='add-damage-expert'),
    path('filterCars/', FilterView.as_view(), name='filter-vehicle'),
    path('filterCarsBuy/', FilterForBuyingView.as_view(), name='filter-vehicle-buy'),
    path("logout/", LogoutView.as_view(), name="logout")
]