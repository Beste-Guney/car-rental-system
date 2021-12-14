from django.urls import path
from manager.views import ManagerMainPage, BranchCarView, ajaxBuyCar, BuyCarView, EmployeeView, filter_car_by_age, AddBranchEmployeeView,AddChauffeurView, AddDamageExpertView

app_name = 'manager'
urlpatterns = [
    path('managerDashboard/<int:manager_id>', ManagerMainPage.as_view(), name='manager_dashboard'),
    path('branchCars/<int:branch_id>', BranchCarView.as_view(), name='cars_at_branch'),
    path('buyCar/<int:branch_id>', BuyCarView.as_view(), name='buy-available-cars'),
    path('ajax/buyCar', ajaxBuyCar, name='ajax_buy_car'),
    path('employeeList/<int:branch_id>', EmployeeView.as_view(), name='branch-employees'),
    path('addBranchEmployee/', AddBranchEmployeeView.as_view(), name='add-branch-employee'),
    path('addChauffeur/', AddChauffeurView.as_view(), name='add-chauffeur'),
    path('addDamageExpert/', AddDamageExpertView.as_view(), name='add-damage-expert'),
    path('filterByAge/<int:value>', filter_car_by_age, name='filter-by-age')
]