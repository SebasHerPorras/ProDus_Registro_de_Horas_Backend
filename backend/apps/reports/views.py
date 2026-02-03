"""
Views para el módulo de reportes.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime, timedelta

from core.permissions import IsProjectCoordinator, IsGeneralCoordinator
from .models import DayReported, DayReportHistory
from .serializers import (
    DayReportedSerializer,
    DayReportedCreateSerializer,
    DayReportedApprovalSerializer,
    DayReportHistorySerializer,
    DayReportedBulkCreateSerializer
)
from .services import DayReportService


class DayReportedViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestión de reportes diarios.
    """
    queryset = DayReported.objects.select_related('activity', 'user', 'user__person').all()
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DayReportedCreateSerializer
        if self.action == 'bulk_create':
            return DayReportedBulkCreateSerializer
        if self.action in ['approve', 'reject']:
            return DayReportedApprovalSerializer
        return DayReportedSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = DayReported.objects.select_related('activity', 'user', 'user__person')
        
        # Filtros por query params
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        status_filter = self.request.query_params.get('status')
        user_id = self.request.query_params.get('user_id')
        
        # Admin y coordinadores pueden ver todos
        if user.is_admin or (hasattr(user, 'person') and user.person.role in ['PROJECT_COORDINATOR', 'GENERAL_COORDINATOR']):
            if user_id:
                queryset = queryset.filter(user_id=user_id)
        else:
            # Usuarios normales solo ven sus propios reportes
            queryset = queryset.filter(user=user)
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset.order_by('-date', '-start_time')
    
    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """
        Crea múltiples reportes a la vez.
        """
        serializer = DayReportedBulkCreateSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        reports = serializer.save()
        
        return Response(
            DayReportedSerializer(reports, many=True).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        """
        Aprueba un reporte.
        Solo coordinadores pueden aprobar.
        """
        # Verificar permisos
        user = request.user
        if not user.is_admin and not (hasattr(user, 'person') and user.person.role in ['PROJECT_COORDINATOR', 'GENERAL_COORDINATOR']):
            return Response(
                {'error': 'No tiene permisos para aprobar reportes.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = DayReportedApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            report = DayReportService.approve_report(
                report_id=pk,
                approved_by_user=user,
                notes=serializer.validated_data.get('notes', '')
            )
            return Response(DayReportedSerializer(report).data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except DayReported.DoesNotExist:
            return Response({'error': 'Reporte no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        """
        Rechaza un reporte.
        Solo coordinadores pueden rechazar.
        """
        user = request.user
        if not user.is_admin and not (hasattr(user, 'person') and user.person.role in ['PROJECT_COORDINATOR', 'GENERAL_COORDINATOR']):
            return Response(
                {'error': 'No tiene permisos para rechazar reportes.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = DayReportedApprovalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        notes = serializer.validated_data.get('notes', '')
        if not notes:
            return Response(
                {'error': 'Debe proporcionar una razón para el rechazo.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            report = DayReportService.reject_report(
                report_id=pk,
                rejected_by_user=user,
                notes=notes
            )
            return Response(DayReportedSerializer(report).data)
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except DayReported.DoesNotExist:
            return Response({'error': 'Reporte no encontrado.'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Obtiene reportes pendientes de aprobación.
        Solo para coordinadores.
        """
        user = request.user
        if not user.is_admin and not (hasattr(user, 'person') and user.person.role in ['PROJECT_COORDINATOR', 'GENERAL_COORDINATOR']):
            return Response(
                {'error': 'No tiene permisos para ver reportes pendientes.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        reports = DayReportService.get_pending_reports()
        serializer = DayReportedSerializer(reports, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_summary(self, request):
        """
        Obtiene resumen de horas del usuario autenticado.
        """
        user = request.user
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        if not start_date or not end_date:
            # Por defecto, mes actual
            today = timezone.now().date()
            start_date = today.replace(day=1)
            end_date = (start_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        
        total_hours = DayReportService.calculate_hours_by_user_and_period(
            user.id, start_date, end_date
        )
        
        summary_by_activity = DayReportService.get_summary_by_activity(
            user.id, start_date, end_date
        )
        
        return Response({
            'user_id': user.id,
            'start_date': start_date,
            'end_date': end_date,
            'total_approved_hours': total_hours,
            'by_activity': summary_by_activity
        })


class DayReportHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet de solo lectura para historial de reportes.
    """
    queryset = DayReportHistory.objects.select_related(
        'day_report', 'changed_by_user', 'activity'
    ).all()
    serializer_class = DayReportHistorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        queryset = DayReportHistory.objects.select_related(
            'day_report', 'changed_by_user', 'activity'
        )
        
        # Filtrar por report_id si se proporciona
        report_id = self.request.query_params.get('report_id')
        if report_id:
            queryset = queryset.filter(day_report_id=report_id)
        
        # Admin puede ver todo
        if user.is_admin:
            return queryset
        
        # Coordinadores pueden ver historial de sus asistentes
        if hasattr(user, 'person') and user.person.role in ['PROJECT_COORDINATOR', 'GENERAL_COORDINATOR']:
            return queryset
        
        # Usuarios normales solo ven historial de sus propios reportes
        return queryset.filter(day_report__user=user)
