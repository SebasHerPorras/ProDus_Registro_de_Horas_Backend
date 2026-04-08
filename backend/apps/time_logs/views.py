from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError

from apps.ip_control.services import validate_ip_access
from apps.time_logs.services import create_time_log_entry
from apps.time_logs.serializers import TimeLogSerializer


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