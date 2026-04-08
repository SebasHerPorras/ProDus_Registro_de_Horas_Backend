from django.core.exceptions import ValidationError


def validate_ip_access(ip_address):
    """
    Valida si la IP está autorizada para acceder.
    
    De momento: siempre retorna True (simulado).
    Luego: consultará AuthorizedIp y IpException.
    
    Args:
        ip_address (str): IP del cliente (ej: '10.233.194.99')
    
    Returns:
        bool: True si está autorizada
    
    Raises:
        ValidationError: Si no está autorizada
    """
    # TODO: implementar validación real
    # 1. Verificar si IP está en AuthorizedIp.is_active=True
    # 2. Verificar si usuario está en excepción activa
    # 3. Retornar True/False o lanzar ValidationError
    
    return True