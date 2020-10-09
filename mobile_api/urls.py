from django.urls import path
from . import views


urlpatterns = [
    path("", views.IncidentListAPIView.as_view(), name="incidents"),
    path("<int:id>", views.IncidentDetailAPIView.as_view(),
         name="incident-detail"),
]
