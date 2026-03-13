"""
Permisos personalizados para el proyecto.
"""
from rest_framework.permissions import BasePermission
from apps.login.validators import is_valid_institute_ip


class IsFromInstitute(BasePermission):
    """
    Permiso que verifica que la petición venga desde la IP del instituto.
    """
    message = "Acceso denegado. Debe conectarse desde la red del instituto."
    
    def has_permission(self, request, view):
        return is_valid_institute_ip(request)


class IsAdmin(BasePermission):
    """
    Permiso que verifica que el usuario sea administrador.
    """
    message = "Se requieren permisos de administrador."
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_admin


class IsProjectCoordinator(BasePermission):
    """
    Permiso para coordinadores de proyecto.
    Pueden aprobar/rechazar/modificar actividades de asistentes.
    """
    message = "Se requieren permisos de coordinador de proyecto."
    
    def has_permission(self, request, view):
        return False


class IsGeneralCoordinator(BasePermission):
    """
    Permiso para coordinador general.
    Supervisor general del sistema.
    """
    message = "Se requieren permisos de coordinador general."
    
    def has_permission(self, request, view):
        return False


class IsAssistant(BasePermission):
    """
    Permiso para asistentes.
    """
    message = "Se requieren permisos de asistente."
    
    def has_permission(self, request, view):
        return False
