"""
Servicios de lógica de negocio para usuarios.
"""
from django.db import transaction
from .models import User, Person, Assistant


class UserService:
    """
    Servicio para operaciones de usuarios.
    """
    
    @staticmethod
    def get_user_by_username(username: str):
        """Obtiene un usuario por su username."""
        return User.objects.filter(username=username).first()
    
    @staticmethod
    def get_active_users():
        """Obtiene todos los usuarios activos."""
        return User.objects.filter(is_active=True)
    
    @staticmethod
    @transaction.atomic
    def create_assistant(username: str, password: str, name: str, degree: str, hire_date) -> Assistant:
        """
        Crea un asistente completo (User + Person + Assistant).
        """
        user = User.objects.create_user(
            username=username,
            password=password
        )
        
        Person.objects.create(
            user=user,
            name=name,
            role=Person.RoleChoices.ASSISTANT
        )
        
        assistant = Assistant.objects.create(
            user=user,
            degree=degree,
            hire_date=hire_date
        )
        
        return assistant
    
    @staticmethod
    @transaction.atomic
    def create_coordinator(username: str, password: str, name: str, role: str) -> Person:
        """
        Crea un coordinador (User + Person).
        """
        user = User.objects.create_user(
            username=username,
            password=password
        )
        
        person = Person.objects.create(
            user=user,
            name=name,
            role=role
        )
        
        return person


class AssistantService:
    """
    Servicio para operaciones de asistentes.
    """
    
    @staticmethod
    def get_all_assistants():
        """Obtiene todos los asistentes."""
        return Assistant.objects.select_related('user', 'user__person').filter(is_active=True)
    
    @staticmethod
    def get_assistant_by_user_id(user_id: int):
        """Obtiene un asistente por ID de usuario."""
        return Assistant.objects.select_related('user', 'user__person').filter(user_id=user_id).first()
    
    @staticmethod
    def get_assistants_by_coordinator(coordinator_user_id: int):
        """
        Obtiene los asistentes supervisados por un coordinador.
        """
        return Assistant.objects.select_related('user', 'user__person').filter(
            supervisor_id=coordinator_user_id,
            is_active=True
        )
