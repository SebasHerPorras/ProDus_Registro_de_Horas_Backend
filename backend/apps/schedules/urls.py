"""
URLs del módulo de horarios.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduleViewSet, ScheduleDayViewSet

router = DefaultRouter()
router.register(r'schedules', ScheduleViewSet, basename='schedule')
router.register(r'schedule-days', ScheduleDayViewSet, basename='schedule-day')

urlpatterns = [
    path('', include(router.urls)),
]
