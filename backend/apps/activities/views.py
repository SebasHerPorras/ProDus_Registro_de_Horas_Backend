"""
Views para el módulo de actividades.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsAdmin
from .models import Activity
from .serializers import ActivitySerializer


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de actividades.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Solo mostrar actividades activas a usuarios normales
        if self.request.user.is_admin:
            return Activity.objects.all()
        return Activity.objects.filter(is_active=True)
    
    def get_permissions(self):
        # Solo admin puede crear/editar/eliminar
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdmin()]
        return [IsAuthenticated()]
