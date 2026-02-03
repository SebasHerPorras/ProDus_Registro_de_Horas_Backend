"""
Views/Endpoints para el módulo de usuarios.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from core.permissions import IsAdmin, IsFromInstitute
from core.validators import get_client_ip, is_valid_institute_ip
from decouple import config
from .models import User, Person, Assistant
from .serializers import (
    UserSerializer, 
    PersonSerializer, 
    AssistantSerializer,
    AssistantCreateSerializer,
    CustomTokenObtainPairSerializer
)
from .services import UserService, AssistantService


@api_view(['GET'])
@permission_classes([AllowAny])
def check_ip(request):
    """
    Endpoint para verificar si la IP del cliente está permitida.
    No requiere autenticación.
    """
    client_ip = get_client_ip(request)
    is_allowed = is_valid_institute_ip(request)
    dev_mode = config('ALLOW_ALL_IPS', default=True, cast=bool)
    
    return Response({
        'allowed': is_allowed,
        'dev_mode': dev_mode,
        'client_ip': client_ip
    })


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para obtener tokens JWT.
    Incluye validación de IP del instituto.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny, IsFromInstitute]  # Validar IP del instituto
    
    def post(self, request, *args, **kwargs):
        # Obtener IP del cliente para logging
        client_ip = get_client_ip(request)
        
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            # Agregar IP a la respuesta para debugging
            response.data['client_ip'] = client_ip
        
        return response


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de usuarios.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Obtiene el perfil del usuario autenticado.
        """
        serializer = UserSerializer(request.user)
        data = serializer.data
        
        if hasattr(request.user, 'person'):
            data['person'] = PersonSerializer(request.user.person).data
        
        if hasattr(request.user, 'assistant'):
            data['assistant'] = AssistantSerializer(request.user.assistant).data
        
        return Response(data)


class AssistantViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de asistentes.
    """
    queryset = Assistant.objects.select_related('user', 'user__person').all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return AssistantCreateSerializer
        return AssistantSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        # Si es admin, puede ver todos
        if user.is_admin:
            return AssistantService.get_all_assistants()
        
        # Si es coordinador, puede ver los asistentes que supervisa
        if hasattr(user, 'person') and user.person.role in ['PROJECT_COORDINATOR', 'GENERAL_COORDINATOR']:
            return AssistantService.get_assistants_by_coordinator(user.id)
        
        # Si es asistente, solo puede verse a sí mismo
        if hasattr(user, 'assistant'):
            return Assistant.objects.filter(user=user)
        
        return Assistant.objects.none()
