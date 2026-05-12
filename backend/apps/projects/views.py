from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.projects.models import Project
from apps.projects.serializers import ActiveProjectSerializer, ActiveCoordinatorSerializer
from apps.users.models import User


class ActiveProjectListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Project.objects.filter(is_active=True).order_by('name')
        serializer = ActiveProjectSerializer(queryset, many=True)
        return Response({'ok': True, 'results': serializer.data})


class ActiveCoordinatorListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = User.objects.select_related('role').filter(
            is_active=True,
            role__code__in=['coordinador', 'coordinator'],
        ).order_by('full_name', 'username')
        serializer = ActiveCoordinatorSerializer(queryset, many=True)
        return Response({'ok': True, 'results': serializer.data})