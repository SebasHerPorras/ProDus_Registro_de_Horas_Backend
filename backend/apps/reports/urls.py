"""
URLs del módulo de reportes.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DayReportedViewSet, DayReportHistoryViewSet

router = DefaultRouter()
router.register(r'reports', DayReportedViewSet, basename='day-report')
router.register(r'report-history', DayReportHistoryViewSet, basename='report-history')

urlpatterns = [
    path('', include(router.urls)),
]
