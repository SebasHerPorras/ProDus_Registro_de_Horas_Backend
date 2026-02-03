"""
Views para el módulo de horarios.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsAdmin
from .models import Schedule, ScheduleDay
from .serializers import ScheduleSerializer, ScheduleDaySerializer, ScheduleCreateSerializer


class ScheduleViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de horarios.
    """
    queryset = Schedule.objects.select_related('user').all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action in ['create', 'update']:
            return ScheduleCreateSerializer
        return ScheduleSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin:
            return Schedule.objects.select_related('user').all()
        
        # Usuarios normales solo ven su propio horario
        return Schedule.objects.filter(user=user)


class ScheduleDayViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de días de horario.
    """
    queryset = ScheduleDay.objects.select_related('user').all()
    serializer_class = ScheduleDaySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        
        if user.is_admin:
            return ScheduleDay.objects.select_related('user').all()
        
        return ScheduleDay.objects.filter(user=user)
