from django.core.exceptions import ValidationError

from .validators import get_client_ip, is_valid_institute_ip


def validate_institute_ip_addr(request):
    client_ip = get_client_ip(request)
    is_allowed = is_valid_institute_ip(request)

    return {
        'allowed': is_allowed,
        'client_ip': client_ip,
        'message': 'Acceso permitido' if is_allowed else 'Acceso denegado - IP no autorizada',
    }


def change_user_password(user, current_password, new_password, neet_force_change):
    if not user.check_password(current_password):
        raise ValidationError({'current_password': 'La contraseña actual es incorrecta.'})

    user.set_password(new_password)
    user.needs_password_change = neet_force_change
    user.save(update_fields=['password', 'needs_password_change'])
    return user