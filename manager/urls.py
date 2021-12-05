from django.urls import path
from manager.views import ManagerMainPage, BranchCarView, ajaxBuyCar, BuyCarView

app_name  = 'manager'
urlpatterns = [
    path('managerDashboard/<int:manager_id>', ManagerMainPage.as_view(), name='manager_dashboard'),
    path('branchCars/<int:branch_id>', BranchCarView.as_view(), name='cars_at_branch'),
    path('buyCar', BuyCarView.as_view(), name='buy-available-cars'),
    path('ajax/buyCar', ajaxBuyCar, name='ajax_buy_car'),
]