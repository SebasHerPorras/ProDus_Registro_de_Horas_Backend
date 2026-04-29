from django.urls import path

from .views import create_assistant_schedule_view

urlpatterns = [
    path(
        'schedules/',
        create_assistant_schedule_view,
        name='create_assistant_schedule',
    ),
]
