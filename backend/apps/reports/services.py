"""
Servicios de lógica de negocio para reportes.
"""
from django.db import transaction
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta

from .models import DayReported, DayReportHistory


class DayReportService:
    """
    Servicio para operaciones de reportes diarios.
    """
    
    @staticmethod
    def get_reports_by_user(user_id: int, start_date=None, end_date=None):
        """Obtiene reportes de un usuario en un rango de fechas."""
        queryset = DayReported.objects.filter(user_id=user_id)
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset.select_related('activity', 'user')
    
    @staticmethod
    def get_reports_by_date_range(start_date, end_date, status=None):
        """Obtiene reportes en un rango de fechas."""
        queryset = DayReported.objects.filter(
            date__gte=start_date,
            date__lte=end_date
        )
        
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.select_related('activity', 'user', 'user__person')
    
    @staticmethod
    def get_pending_reports():
        """Obtiene reportes pendientes de aprobación."""
        return DayReported.objects.filter(
            status=DayReported.StatusChoices.PENDING
        ).select_related('activity', 'user', 'user__person')
    
    @staticmethod
    @transaction.atomic
    def approve_report(report_id: int, approved_by_user, notes: str = None):
        """Aprueba un reporte."""
        report = DayReported.objects.select_for_update().get(id=report_id)
        
        if report.status != DayReported.StatusChoices.PENDING:
            raise ValueError("Solo se pueden aprobar reportes pendientes.")
        
        # Crear historial
        DayReportHistory.objects.create(
            day_report=report,
            changed_by_user=approved_by_user,
            new_status=DayReported.StatusChoices.APPROVED,
            notes=notes,
            manager=approved_by_user.username
        )
        
        # Actualizar reporte
        report.status = DayReported.StatusChoices.APPROVED
        report.manager = approved_by_user.username
        report.save()
        
        return report
    
    @staticmethod
    @transaction.atomic
    def reject_report(report_id: int, rejected_by_user, notes: str):
        """Rechaza un reporte."""
        report = DayReported.objects.select_for_update().get(id=report_id)
        
        if report.status != DayReported.StatusChoices.PENDING:
            raise ValueError("Solo se pueden rechazar reportes pendientes.")
        
        # Crear historial
        DayReportHistory.objects.create(
            day_report=report,
            changed_by_user=rejected_by_user,
            new_status=DayReported.StatusChoices.REJECTED,
            notes=notes,
            manager=rejected_by_user.username
        )
        
        # Actualizar reporte
        report.status = DayReported.StatusChoices.REJECTED
        report.manager = rejected_by_user.username
        report.save()
        
        return report
    
    @staticmethod
    def calculate_hours_by_user_and_period(user_id: int, start_date, end_date):
        """Calcula las horas trabajadas por un usuario en un período."""
        reports = DayReported.objects.filter(
            user_id=user_id,
            date__gte=start_date,
            date__lte=end_date,
            status=DayReported.StatusChoices.APPROVED
        )
        
        total_hours = 0
        for report in reports:
            total_hours += report.hours_worked
        
        return total_hours
    
    @staticmethod
    def get_summary_by_activity(user_id: int, start_date, end_date):
        """Obtiene resumen de horas por actividad."""
        reports = DayReported.objects.filter(
            user_id=user_id,
            date__gte=start_date,
            date__lte=end_date
        ).select_related('activity')
        
        summary = {}
        for report in reports:
            activity_name = report.activity.name
            if activity_name not in summary:
                summary[activity_name] = {
                    'activity_id': report.activity.id,
                    'activity_name': activity_name,
                    'category': report.activity.category,
                    'total_hours': 0,
                    'count': 0
                }
            summary[activity_name]['total_hours'] += report.hours_worked
            summary[activity_name]['count'] += 1
        
        return list(summary.values())
