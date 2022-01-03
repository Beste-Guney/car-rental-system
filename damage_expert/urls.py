from django.contrib.auth.views import LogoutView
from django.urls import path
from damage_expert.views import *

app_name = 'damage_expert'
urlpatterns = [
    path('damageExpertDashboard/<int:expert_id>', DamageExpertDashboard.as_view(), name='damage-expert-dashboard'),
    path('review/<int:res_no>', ReviewReservation.as_view(), name='damage-expert-review'),
    path('checkAssigned/<int:expert_id>', CheckAssigned.as_view(), name='damage-expert-check'),
    path('review/', ReviewReservation.as_view(), name='damage-expert-review'),
    path('logout/', LogoutView.as_view(), name='logout')
]