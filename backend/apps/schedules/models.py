from django.db import models
from django.core.exceptions import ValidationError
from django.db.models import Q, F


class Schedule(models.Model):
    assistant = models.ForeignKey(
        'users.Assistant',
        on_delete=models.CASCADE,
        related_name='schedules',
        verbose_name='Asistente'
    )
    valid_from = models.DateField(verbose_name='Válido desde')
    valid_to = models.DateField(null=True, blank=True, verbose_name='Válido hasta')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')

    class Meta:
        db_table = 'schedule'
        verbose_name = 'Horario'
        verbose_name_plural = 'Horarios'

    def __str__(self):
        return f"Horario ({self.valid_from} - {self.valid_to or 'Presente'})"


class ScheduleBlock(models.Model):

    class DayOfWeek(models.TextChoices):
        MONDAY = 'MONDAY', 'Lunes'
        TUESDAY = 'TUESDAY', 'Martes'
        WEDNESDAY = 'WEDNESDAY', 'Miércoles'
        THURSDAY = 'THURSDAY', 'Jueves'
        FRIDAY = 'FRIDAY', 'Viernes'
        SATURDAY = 'SATURDAY', 'Sábado'
        SUNDAY = 'SUNDAY', 'Domingo'

    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        related_name='blocks',
        verbose_name='Horario'
    )

    day_of_week = models.CharField(
        max_length=15,
        choices=DayOfWeek.choices,
        verbose_name='Día de la semana'
    )

    start_time = models.TimeField(verbose_name='Hora de inicio')
    end_time = models.TimeField(verbose_name='Hora de fin')

    class Meta:
        db_table = 'schedule_block'
        verbose_name = 'Bloque de Horario'
        verbose_name_plural = 'Bloques de Horarios'

        constraints = [
            # ✔ No permite duración negativa o cero
            models.CheckConstraint(
                condition=Q(end_time__gt=F('start_time')),
                name='end_after_start_schedule_block'
            ),
        ]

    def clean(self):
        super().clean()

        # ✔ Validación lógica adicional (mensajes claros)
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError(
                    "La hora de fin debe ser mayor a la de inicio (no se permiten bloques que crucen medianoche)."
                )

        # ✔ Validación de traslapes
        overlapping = ScheduleBlock.objects.filter(
            schedule=self.schedule,
            day_of_week=self.day_of_week
        ).exclude(pk=self.pk)

        for block in overlapping:
            if (
                self.start_time < block.end_time and
                self.end_time > block.start_time
            ):
                raise ValidationError(
                    f"Traslape con bloque existente: {block.start_time} - {block.end_time}"
                )

    def save(self, *args, **kwargs):
        # ✔ Asegura que SIEMPRE se valide antes de guardar
        self.full_clean()
        super().save(*args, **kwargs)

    def get_work_minutes(self):
        # ✔ cálculo dinámico (evita inconsistencias)
        from datetime import datetime, date

        delta = (
            datetime.combine(date.min, self.end_time) -
            datetime.combine(date.min, self.start_time)
        )

        return int(delta.total_seconds() // 60)

    def __str__(self):
        return f"{self.get_day_of_week_display()} {self.start_time} - {self.end_time}"