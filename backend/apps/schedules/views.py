from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.permissions import IsAdminOrCoordinator

from .serializers import ScheduleCreateSerializer, ScheduleDetailSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminOrCoordinator])
def create_assistant_schedule_view(request):
    serializer = ScheduleCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    schedule = serializer.save()

    return Response(
        {
            'ok': True,
            'schedule': ScheduleDetailSerializer(schedule).data,
        },
        status=status.HTTP_201_CREATED)
