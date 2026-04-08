from django.db import models


# El modelo TimeLogStatus representa los diferentes estados que un registro de horas puede tener 
# (por ejemplo, pendiente, aprobado, rechazado).
class TimeLogStatus(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Código')
    is_final = models.BooleanField(default=False, verbose_name='¿Es estado final?')

    class Meta:
        db_table = 'time_log_status'
        verbose_name = 'Estado de Registro'
        verbose_name_plural = 'Estados de Registros'
        ordering = ['code']

    def __str__(self):
        return self.code
      
# El modelo TimeLog representa un registro de horas de un asistente, con campos para la entrada, salida,
# descripción del trabajo, minutos de almuerzo usados, estado del registro y detalles de la decisión
# en caso de que el registro sea aprobado o rechazado.
# Utiliza a timelogstatus para definir el estado del registro, lo que permite una gestión flexible de los estados
# (pendiente, aprobado, rechazado, etc.) sin necesidad de modificar el modelo TimeLog cada vez que se agregue un nuevo estado.
class TimeLog(models.Model):
    # referencia al asistente que hizo el registro de horas
    assistant = models.ForeignKey(
        'users.Assistant',
        on_delete=models.CASCADE,
        related_name='timelogs',
        verbose_name='Asistente'
    )
    # atributos de entrada y salida
    # check_in es obligatorio, mientras que check_out es opcional para permitir registros de horas en curso
    # el check in captura la fecha y hora del sistema apenas se crea el registro
    check_in = models.DateTimeField(verbose_name='Entrada')
    check_out = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Salida'
    )
    # descripción del trabajo realizado durante el período registrado -> puede venir en blanco
    work_description = models.TextField(
        blank=True,
        default='',
        verbose_name='Descripción del trabajo'
    )
    # minutos de almuerzo o tiempo de descanso, se resta al total
    break_minutes = models.PositiveIntegerField(
        default=0,
        verbose_name='Minutos de descanso usados'
    )
    status = models.ForeignKey(
        'time_logs.TimeLogStatus',
        on_delete=models.PROTECT,
        verbose_name='Estado'
    )
    decided_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_timelogs',
        verbose_name='Decidido por'
    )
    decided_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de decisión'
    )
    decision_comment = models.TextField(
        blank=True,
        default='',
        verbose_name='Comentario de decisión'
    )

    class Meta:
        db_table = 'time_log'
        verbose_name = 'Registro de Horas'
        verbose_name_plural = 'Registros de Horas'
        ordering = ['-check_in']

    def __str__(self):
        return f"{self.assistant.user.full_name} - {self.check_in}"