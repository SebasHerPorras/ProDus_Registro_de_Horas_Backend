from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from core.permissions import IsAdmin, IsAdminOrCoordinator, IsFromInstitute 

from .models import AllowedIPRange, Assistant, User
from .serializers import (
    AllowedIPRangeSerializer,
    AssistantCreateSerializer,
    CustomTokenObtainPairSerializer,
    UserSerializer,
    AssistantListSerializer,
)

from .services import validate_institute_ip_addr


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def validate_institute_ip_addr_view(request):
    result = validate_institute_ip_addr(request)
    return Response(result)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    return Response({'detail': 'Sesión cerrada correctamente'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    return Response({'ok': True, 'user': UserSerializer(request.user).data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminOrCoordinator])
def create_assistant_view(request):
    serializer = AssistantCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.save()
    return Response({'ok': True, **data}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrCoordinator])
def list_assistants_view(request):
    queryset = Assistant.objects.select_related('user').order_by('user__full_name')
    serializer = AssistantListSerializer(queryset, many=True)
    return Response({'ok': True, 'results': serializer.data}, status=status.HTTP_200_OK)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        return Response({'ok': True, 'user': UserSerializer(request.user).data}, status=status.HTTP_200_OK)


class AllowedIPRangeViewSet(viewsets.ModelViewSet):
    queryset = AllowedIPRange.objects.all().order_by('-is_active', 'network')
    serializer_class = AllowedIPRangeSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
