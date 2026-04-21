from django.utils import timezone
from django.core.exceptions import ValidationError
from asgiref.sync import sync_to_async
from apps.time_logs.models import TimeLog, TimeLogStatus
from apps.projects.models import Project
from apps.users.models import User

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


def close_time_log_entry(assistant, payload=None):
    payload = payload or {}
    active_time_log = get_active_time_log(assistant)

    if not active_time_log:
        raise ValidationError('No tienes una jornada activa para cerrar.')

    closed_status, _ = TimeLogStatus.objects.get_or_create(
        code='CLOSED',
        defaults={'is_final': True},
    )

    project_id = payload.get('project_id')
    manager_user_id = payload.get('manager_user_id')
    notes = payload.get('notes', '')
    activities = payload.get('activities', '')
    break_minutes = payload.get('break_minutes', 0)

    project = None
    if project_id is not None:
        project = Project.objects.filter(id=project_id, is_active=True).first()
        if not project:
            raise ValidationError('Proyecto inválido o inactivo.')

    manager_user = None
    if manager_user_id is not None:
        manager_user = User.objects.filter(
            id=manager_user_id,
            is_active=True,
            role__code__in=['coordinador', 'coordinator'],
        ).first()
        if not manager_user:
            raise ValidationError('Encargado inválido. Debe ser un coordinador activo.')

    # Cierre real con hora de servidor + datos del formulario
    active_time_log.check_out = timezone.now()
    active_time_log.status = closed_status
    active_time_log.project = project
    active_time_log.manager_user = manager_user
    active_time_log.activities = activities
    active_time_log.decision_comment = notes
    active_time_log.break_minutes = break_minutes
    active_time_log.closed_by = TimeLog.ClosedBy.USER

    # Mantener flujo simple: sin metadatos de aprobación en esta fase
    active_time_log.decided_by = None
    active_time_log.decided_at = None

    active_time_log.save(
        update_fields=[
            'check_out',
            'status',
            'project',
            'manager_user',
            'activities',
            'decision_comment',
            'break_minutes',
            'closed_by',
            'decided_by',
            'decided_at',
        ]
    )
    return active_time_log


def _close_open_time_logs_by_system_sync():
    closed_status, _ = TimeLogStatus.objects.get_or_create(
        code='CLOSED',
        defaults={'is_final': True},
    )

    opened_logs = TimeLog.objects.filter(
        status__code='IN_PROGRESS',
        check_out__isnull=True,
    )

    total_opened = opened_logs.count()
    if total_opened == 0:
        return 0

    # Cierre automático de sistema con valores default de formulario.
    opened_logs.update(
        check_out=timezone.now(),
        status=closed_status,
        project=None,
        manager_user=None,
        activities='',
        decision_comment='',
        break_minutes=0,
        closed_by=TimeLog.ClosedBy.SYSTEM,
        decided_by=None,
        decided_at=None,
    )

    return total_opened


async def close_open_time_logs_by_system():
    return await sync_to_async(
        _close_open_time_logs_by_system_sync,
        thread_sensitive=True,
    )()