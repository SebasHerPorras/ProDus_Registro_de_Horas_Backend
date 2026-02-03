"""
Modelos de reportes según el diagrama ER:
- DayReported: Registro de horas diarias
- DayReportHistory: Historial de cambios en reportes
"""
from django.db import models
from apps.users.models import User
from apps.activities.models import Activity


class DayReported(models.Model):
    """
    Modelo Day_Reported - Registro de horas diarias.
    Campos según diagrama: DayReportId, UserId (FK), Activity (FK), StartTime, EndTime, 
    Date, Notes, Status, LastModifiedAt, Manager
    """
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        APPROVED = 'APPROVED', 'Aprobado'
        REJECTED = 'REJECTED', 'Rechazado'
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='day_reports',
        verbose_name='Usuario'
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.PROTECT,
        related_name='day_reports',
        verbose_name='Actividad'
    )
    start_time = models.TimeField(
        verbose_name='Hora de inicio'
    )
    end_time = models.TimeField(
        verbose_name='Hora de fin'
    )
    date = models.DateField(
        verbose_name='Fecha'
    )
    notes = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Notas'
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name='Estado'
    )
    last_modified_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última modificación'
    )
    manager = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Manager que aprobó/rechazó'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    
    class Meta:
        db_table = 'day_reported'
        verbose_name = 'Reporte Diario'
        verbose_name_plural = 'Reportes Diarios'
        ordering = ['-date', '-start_time']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['date']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.activity.name}"
    
    @property
    def hours_worked(self):
        """Calcula las horas trabajadas."""
        from datetime import datetime
        start = datetime.combine(datetime.today(), self.start_time)
        end = datetime.combine(datetime.today(), self.end_time)
        diff = end - start
        return round(diff.total_seconds() / 3600, 2)


class DayReportHistory(models.Model):
    """
    Modelo Day_Report_History - Historial de cambios en reportes.
    Campos según diagrama: HistoryId, DayReportId (FK), ChangedByUserId (FK),
    ActivityId, NewStartTime, NewEndTime, NewStatus, Notes, ChangedAt, Manager
    """
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente'
        APPROVED = 'APPROVED', 'Aprobado'
        REJECTED = 'REJECTED', 'Rechazado'
    
    day_report = models.ForeignKey(
        DayReported,
        on_delete=models.CASCADE,
        related_name='history',
        verbose_name='Reporte'
    )
    changed_by_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='report_changes',
        verbose_name='Modificado por'
    )
    activity = models.ForeignKey(
        Activity,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name='Actividad'
    )
    new_start_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name='Nueva hora de inicio'
    )
    new_end_time = models.TimeField(
        null=True,
        blank=True,
        verbose_name='Nueva hora de fin'
    )
    new_status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        null=True,
        blank=True,
        verbose_name='Nuevo estado'
    )
    notes = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name='Notas del cambio'
    )
    changed_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha del cambio'
    )
    manager = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name='Manager'
    )
    
    class Meta:
        db_table = 'day_report_history'
        verbose_name = 'Historial de Reporte'
        verbose_name_plural = 'Historial de Reportes'
        ordering = ['-changed_at']
        indexes = [
            models.Index(fields=['day_report', 'changed_at']),
        ]
    
    def __str__(self):
        return f"Cambio en {self.day_report} por {self.changed_by_user.username}"
