from django.urls import path
from .views import (
    update_schedule,
)

urlpatterns = [
    path('update/', update_schedule, name="update"),
]