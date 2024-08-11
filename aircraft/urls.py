from django.urls import path
from . import views

from .views import AircraftView

urlpatterns = [
    path('', AircraftView.as_view()),
    path('<int:id>', AircraftView.as_view()),
]
