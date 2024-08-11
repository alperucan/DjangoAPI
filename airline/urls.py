from django.urls import path

from .views import AirlineView

urlpatterns = [
    path('', AirlineView.as_view()),
    path('<int:id>', AirlineView.as_view()),
]
