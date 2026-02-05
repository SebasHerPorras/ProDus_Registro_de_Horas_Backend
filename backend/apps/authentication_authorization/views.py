"""
Views/Endpoints para autenticación y autorización.
"""
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .services import validate_institute_ip_addr
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def validate_institute_ip_addr_view(request):
    """
    Endpoint que valida si la IP del cliente pertenece a la red del instituto.
    Siempre usa la IP real del cliente (REMOTE_ADDR) para mayor seguridad.
    """
    result = validate_institute_ip_addr(request)
    return Response(result)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vista personalizada para obtener tokens JWT.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]
