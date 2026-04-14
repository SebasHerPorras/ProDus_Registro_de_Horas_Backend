from django.utils import timezone
from django.core.exceptions import ValidationError
from apps.time_logs.models import TimeLog, TimeLogStatus


def create_time_log_entry(assistant):
    """
    Crea un nuevo registro de TimeLog cuando el asistente inicia jornada.
    
    Validaciones:
    - No debe haber un TimeLog activo (status='IN_PROGRESS') para este asistente
    
    Args:
        assistant (Assistant): El asistente que inicia jornada
    
    Returns:
        TimeLog: El nuevo registro creado
    
    Raises:
        ValidationError: Si ya hay una jornada activa
    """
    
    # Verificar en BD si ya existe una jornada activa para el asistente.
    active_log = get_active_time_log(assistant)
    
    if active_log:
        raise ValidationError(
            "Ya tienes una jornada activa. Finalízala antes de iniciar una nueva."
        )
    
    # Obtener o crear el status 'IN_PROGRESS'
    in_progress_status, _ = TimeLogStatus.objects.get_or_create(
        code='IN_PROGRESS',
        defaults={'is_final': False}
    )
    
    # Crear el TimeLog
    time_log = TimeLog.objects.create(
        assistant=assistant,
        check_in=timezone.now(),
        status=in_progress_status,
        work_description='',
        break_minutes=0
    )
    
    return time_log


def get_active_time_log(assistant):
    return TimeLog.objects.filter(
        assistant=assistant,
        status__code='IN_PROGRESS',
        check_out__isnull=True,
    ).order_by('-check_in').first()


def get_current_time_log_state(assistant):
    active_time_log = get_active_time_log(assistant)

    if not active_time_log:
        return {
            'active_session': False,
            'session': None,
            'server_now': timezone.now(),
        }

    elapsed_seconds = int((timezone.now() - active_time_log.check_in).total_seconds())

    return {
        'active_session': True,
        'session': active_time_log,
        'server_now': timezone.now(),
        'elapsed_seconds': elapsed_seconds,
    }


def close_time_log_entry(assistant):
    active_time_log = get_active_time_log(assistant)

    if not active_time_log:
        raise ValidationError('No tienes una jornada activa para cerrar.')

    closed_status, _ = TimeLogStatus.objects.get_or_create(
        code='CLOSED',
        defaults={'is_final': True},
    )

    # Cierre básico: la jornada se cierra con hora servidor y sin metadatos de aprobación.
    active_time_log.check_out = timezone.now()
    active_time_log.status = closed_status
    active_time_log.break_minutes = 0
    active_time_log.decided_by = None
    active_time_log.decided_at = None
    active_time_log.decision_comment = ''

    active_time_log.save(
        update_fields=[
            'check_out',
            'status',
            'break_minutes',
            'decided_by',
            'decided_at',
            'decision_comment',
        ]
    )
    return active_time_log