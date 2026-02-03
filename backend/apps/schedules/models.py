"""
Modelos de horarios según el diagrama ER:
- Schedule: Horas por semana del usuario
- Schedule_Day: Detalle de horario por día
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.users.models import User


class Schedule(models.Model):
    """
    Modelo Schedule - Horas semanales del usuario.
    Campos según diagrama: UserId (FK), HoursPerWeek
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='schedule',
        verbose_name='Usuario'
    )
    hours_per_week = models.PositiveIntegerField(
        verbose_name='Horas por semana',
        validators=[MinValueValidator(1), MaxValueValidator(48)]
    )
    
    class Meta:
        db_table = 'schedule'
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'
    
    def __str__(self):
        return f"{self.user.username} - {self.hours_per_week}h/semana"


class ScheduleDay(models.Model):
    """
    Modelo Schedule_Day - Detalle de horario por día.
    Campos según diagrama: ScheduleDayId, UserId (FK), DayNumber, StartTime, EndTime, HoursPerDay
    """
    class DayChoices(models.IntegerChoices):
        MONDAY = 1, 'Lunes'
        TUESDAY = 2, 'Martes'
        WEDNESDAY = 3, 'Miércoles'
        THURSDAY = 4, 'Jueves'
        FRIDAY = 5, 'Viernes'
        SATURDAY = 6, 'Sábado'
        SUNDAY = 7, 'Domingo'
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='schedule_days',
        verbose_name='Usuario'
    )
    day_number = models.PositiveSmallIntegerField(
        choices=DayChoices.choices,
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name='Día de la semana'
    )
    start_time = models.TimeField(
        verbose_name='Hora de inicio'
    )
    end_time = models.TimeField(
        verbose_name='Hora de fin'
    )
    hours_per_day = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name='Horas por día'
    )
    
    class Meta:
        db_table = 'schedule_day'
        verbose_name = 'Día de horario'
        verbose_name_plural = 'Días de horario'
        unique_together = ['user', 'day_number']
        ordering = ['user', 'day_number']
    
    def __str__(self):
        return f"{self.user.username} - {self.get_day_number_display()}: {self.start_time} - {self.end_time}"
    
    def save(self, *args, **kwargs):
        # Calcular horas automáticamente si no se proporcionan
        if not self.hours_per_day:
            from datetime import datetime, timedelta
            start = datetime.combine(datetime.today(), self.start_time)
            end = datetime.combine(datetime.today(), self.end_time)
            diff = end - start
            self.hours_per_day = diff.total_seconds() / 3600
        super().save(*args, **kwargs)
