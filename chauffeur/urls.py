from django.urls import path

from django.contrib.auth.views import LogoutView

from chauffeur.views import ChauffeurDashboard, accept_request, decline_request


app_name = 'chauffeur'
urlpatterns = [
    path('chauffeurDashboard/', ChauffeurDashboard.as_view(), name='chauffeur_dashboard'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('ajaxAcceptRequest/', accept_request, name='accept-request'),
    path('ajaxDeclineRequest/', decline_request, name='decline-request')
]
