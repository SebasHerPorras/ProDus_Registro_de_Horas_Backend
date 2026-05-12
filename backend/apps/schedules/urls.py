from django.urls import path

from .views import create_assistant_schedule_view

urlpatterns = [
    path('create/', create_assistant_schedule_view, name='create_assistant_schedule'),
]
