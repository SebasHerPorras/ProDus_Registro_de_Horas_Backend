from apps.authentication_authorization.validators import is_valid_institute_ip, get_client_ip
import ipaddress

def validate_institute_ip_addr(request):
    """
    Valida si la IP del cliente (REMOTE_ADDR) pertenece a los rangos permitidos.
    Retorna un diccionario con el estado de validación.
    """
    client_ip = get_client_ip(request)
    is_allowed = is_valid_institute_ip(request)
    
    print(f"[IP Validation] Cliente IP: {client_ip}, Permitido: {is_allowed}")
    
    return {
        'allowed': is_allowed,
        'client_ip': client_ip,
        'message': 'Acceso permitido' if is_allowed else 'Acceso denegado - IP no autorizada'
    }
