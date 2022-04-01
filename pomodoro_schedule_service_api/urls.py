from django.urls import path, include
from .views import (
    ScheduleApiView,
)

urlpatterns = [
    path('api/', ScheduleApiView.as_view()),
]