from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.ip_control.services import validate_ip_access
from apps.time_logs.services import (
    create_time_log_entry,
    close_time_log_entry,
    get_current_time_log_state,
)
from apps.time_logs.serializers import (
    TimeLogSerializer,
    WorkSessionCloseInputSerializer,
)


class WorkSessionStartView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """
        POST /api/timelogs/work-session/start/
        
        Inicia una jornada laboral para el usuario autenticado.
        """
        
        # 1. Obtener IP del request
        ip_address = request.META.get('REMOTE_ADDR')
        
        # 2. Validar que IP esté autorizada
        try:
            validate_ip_access(ip_address)
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 3. Obtener asistente del usuario autenticado
        try:
            assistant = request.user.assistant
        except Exception:
            return Response(
                {'error': 'No eres un asistente registrado en el sistema.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # 4. Crear TimeLog
        try:
            time_log = create_time_log_entry(assistant)
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # 5. Serializar y retornar
        serializer = TimeLogSerializer(time_log)
        return Response(
            {'ok': True, 'session': serializer.data},
            status=status.HTTP_200_OK
        )


class WorkSessionCurrentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            assistant = request.user.assistant
        except Exception:
            return Response(
                {
                    'ok': True,
                    'active_session': False,
                    'server_now': timezone.now(),
                    'session': None,
                },
                status=status.HTTP_200_OK
            )

        current_state = get_current_time_log_state(assistant)

        if not current_state['active_session']:
            return Response(
                {
                    'ok': True,
                    'active_session': False,
                    'server_now': timezone.now(),
                    'session': None,
                },
                status=status.HTTP_200_OK
            )

        serializer = TimeLogSerializer(current_state['session'])
        return Response(
            {
                'ok': True,
                'active_session': True,
                'server_now': current_state['server_now'],
                'elapsed_seconds': current_state['elapsed_seconds'],
                'session': serializer.data,
            },
            status=status.HTTP_200_OK
        )


class WorkSessionCloseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            assistant = request.user.assistant
        except Exception:
            return Response(
                {'error': 'No eres un asistente registrado en el sistema.'},
                status=status.HTTP_403_FORBIDDEN
            )

        payload_serializer = WorkSessionCloseInputSerializer(data=request.data)
        payload_serializer.is_valid(raise_exception=True)

        try:
            time_log = close_time_log_entry(
                assistant,
                payload=payload_serializer.validated_data,
            )
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TimeLogSerializer(time_log)
        return Response(
            {
                'ok': True,
                'closed_session': serializer.data,
                'server_now': timezone.now(),
            },
            status=status.HTTP_200_OK
        )