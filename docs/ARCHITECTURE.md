# Este archivo ha sido movido a docs/ARCHITECTURE.md

## 📋 Resumen Ejecutivo

Este documento describe la arquitectura **Monolito Django Modular** elegida para el sistema de Registro de Horas de ProDus, integrado con el portal WordPress del instituto.

---

## 🎯 Arquitectura Elegida: Monolito Django Modular

### ¿Qué es?

Es una arquitectura que organiza todo el código en un solo proyecto Django, pero **separado en módulos (apps) independientes** con responsabilidades claras. Combina la simplicidad del monolito con la organización de arquitecturas más complejas.

```
┌─────────────────────────────────────────────────────────────┐
│                    MONOLITO DJANGO                          │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │    Auth     │  │  Employees  │  │    Time Entries     │  │
│  │   Module    │  │   Module    │  │       Module        │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐    │
│  │                    CORE (Compartido)                │    │
│  │         Permissions | Validators | Exceptions       │    │
│  └─────────────────────────────────────────────────────┘    │
├─────────────────────────────────────────────────────────────┤
│                   Django REST Framework                     │
│                   + JWT Authentication                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🤔 ¿Por Qué Esta Arquitectura es Óptima?

### Alternativas Consideradas

| Arquitectura | Pros | Contras | Veredicto |
|--------------|------|---------|-----------|
| **Monolito Simple** | Muy rápido de desarrollar | Difícil de mantener cuando crece | ❌ |
| **Clean Architecture** | Muy desacoplado, testeable | Sobreingeniería para este proyecto | ❌ |
| **Microservicios** | Escala independiente | Complejidad operacional innecesaria | ❌ |
| **Monolito Modular** ✅ | Balance perfecto | Ninguno significativo para este caso | ✅ |

### Razones de la Elección

#### 1. **Tamaño del Proyecto**
- Sistema de registro de horas con ~3-5 módulos
- Equipo pequeño de desarrollo
- No requiere escalar a millones de usuarios

#### 2. **Integración con WordPress**
- Se embebe en iframe dentro de WordPress
- Un solo backend simplifica la integración
- JWT permite autenticación stateless ideal para iframes

#### 3. **Aprovecha Django al Máximo**
- ORM potente (no necesitamos capa de repositorio extra)
- Admin panel gratuito para gestión
- Sistema de permisos incorporado
- Migraciones automáticas de BD

#### 4. **Mantenibilidad**
- Código organizado por dominio de negocio
- Fácil de entender para nuevos desarrolladores
- Cada módulo puede evolucionar independientemente

#### 5. **Escalabilidad Futura**
- Si el proyecto crece, los módulos pueden extraerse a microservicios
- La separación en apps facilita esta migración

---

## 📁 Estructura de Carpetas

```
ProDus_Registro_de_Horas_Backend/
│
├── backend/
│   ├── manage.py                    # Entry point Django
│   ├── requirements.txt             # Dependencias Python
│   │
│   ├── backend/                     # ⚙️ CONFIGURACIÓN
│   │   ├── __init__.py
│   │   ├── settings.py              # Configuración Django
│   │   ├── urls.py                  # Rutas principales
│   │   ├── wsgi.py                  # Deploy WSGI
│   │   └── asgi.py                  # Deploy ASGI (async)
│   │
│   ├── apps/                        # 📦 MÓDULOS DE NEGOCIO
│   │   ├── __init__.py
│   │   │
│   │   ├── authentication/          # 🔐 Autenticación
│   │   │   ├── __init__.py
│   │   │   ├── models.py            # Modelo User extendido
│   │   │   ├── serializers.py       # DTOs (Login, Register)
│   │   │   ├── views.py             # Endpoints API
│   │   │   ├── services.py          # Lógica de negocio
│   │   │   ├── urls.py              # Rutas del módulo
│   │   │   └── tests.py             # Tests unitarios
│   │   │
│   │   ├── employees/               # 👥 Gestión de Empleados
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── serializers.py
│   │   │   ├── views.py
│   │   │   ├── services.py
│   │   │   ├── urls.py
│   │   │   └── tests.py
│   │   │
│   │   └── time_entries/            # ⏱️ Registro de Horas
│   │       ├── __init__.py
│   │       ├── models.py
│   │       ├── serializers.py
│   │       ├── views.py
│   │       ├── services.py
│   │       ├── urls.py
│   │       └── tests.py
│   │
│   └── core/                        # 🔧 CÓDIGO COMPARTIDO
│       ├── __init__.py
│       ├── permissions.py           # Permisos personalizados
│       ├── exceptions.py            # Excepciones custom
│       ├── validators.py            # Validadores (IP, etc.)
│       └── pagination.py            # Configuración paginación
│
└── venv/                            # Entorno virtual Python
```

---

## 🔄 Flujo de una Petición

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Frontend   │     │    Django    │     │   Database   │
│   (Vue.js)   │     │   Backend    │     │   (SQLite)   │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       │  1. HTTP Request   │                    │
       │  + JWT Token       │                    │
       │───────────────────►│                    │
       │                    │                    │
       │              2. urls.py                 │
       │              (routing)                  │
       │                    │                    │
       │              3. views.py                │
       │              (controlador)              │
       │                    │                    │
       │              4. services.py             │
       │              (lógica negocio)           │
       │                    │                    │
       │              5. models.py               │
       │              (ORM Query)                │
       │                    │───────────────────►│
       │                    │                    │
       │                    │◄───────────────────│
       │              6. serializers.py          │
       │              (formato respuesta)        │
       │                    │                    │
       │  7. JSON Response  │                    │
       │◄───────────────────│                    │
       │                    │                    │
```

---

## 🔐 Autenticación con JWT

### ¿Por qué JWT?

| Característica | Sesiones (Cookies) | JWT ✅ |
|----------------|-------------------|--------|
| Stateless | ❌ Requiere BD | ✅ Token auto-contenido |
| Iframe compatible | ❌ Problemas CORS | ✅ Headers Authorization |
| Escalabilidad | ❌ Sesiones en servidor | ✅ Sin estado en servidor |
| Mobile friendly | ❌ Cookies complicadas | ✅ Fácil implementación |

### Flujo de Autenticación

```
┌─────────────────────────────────────────────────────────────────┐
│                     FLUJO JWT                                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. LOGIN                                                       │
│  ┌────────┐  POST /api/auth/login/   ┌────────┐                │
│  │ Vue.js │ ─────────────────────────► Django │                │
│  │        │  {email, password}       │        │                │
│  └────────┘                          └───┬────┘                │
│                                          │                      │
│                                    Valida IP ✓                  │
│                                    Valida credenciales ✓        │
│                                          │                      │
│  ┌────────┐  {access, refresh}      ┌───┴────┐                │
│  │ Vue.js │ ◄───────────────────────│ Django │                │
│  │        │                         │        │                │
│  └───┬────┘                         └────────┘                │
│      │                                                         │
│      │ Guarda tokens en localStorage                           │
│      │                                                         │
│  2. PETICIONES AUTENTICADAS                                    │
│  ┌────────┐  GET /api/time-entries/  ┌────────┐               │
│  │ Vue.js │ ─────────────────────────► Django │               │
│  │        │  Header: Bearer <token>  │        │               │
│  └────────┘                          └───┬────┘               │
│                                          │                     │
│                                    Valida JWT ✓                │
│                                    Extrae user_id              │
│                                          │                     │
│  ┌────────┐  {data: [...]}          ┌───┴────┐               │
│  │ Vue.js │ ◄───────────────────────│ Django │               │
│  │        │                         │        │                │
│  └────────┘                         └────────┘               │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ ORM de Django

### ¿Por qué usar el ORM nativo?

En lugar de crear una capa de Repository como en .NET, aprovechamos el ORM de Django que ya incluye:

| Patrón .NET | Equivalente Django | Incluido |
|-------------|-------------------|----------|
| DbContext | `django.db.connection` | ✅ Sí |
| Repository | `Model.objects` (Manager) | ✅ Sí |
| Unit of Work | `transaction.atomic()` | ✅ Sí |
| Migrations | `makemigrations` / `migrate` | ✅ Sí |

### Ejemplo Práctico

```python
# models.py - Definición del modelo
class TimeEntry(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    hours = models.DecimalField(max_digits=4, decimal_places=2)
    description = models.TextField()
    
    class Meta:
        verbose_name_plural = "Time Entries"

# services.py - Lógica de negocio usando el ORM
class TimeEntryService:
    @staticmethod
    def get_entries_by_employee(employee_id: int, month: int, year: int):
        return TimeEntry.objects.filter(
            employee_id=employee_id,
            date__month=month,
            date__year=year
        ).select_related('employee')
    
    @staticmethod
    def calculate_monthly_hours(employee_id: int, month: int, year: int):
        result = TimeEntry.objects.filter(
            employee_id=employee_id,
            date__month=month,
            date__year=year
        ).aggregate(total=Sum('hours'))
        return result['total'] or 0
```

---

## 🌐 Validación de IP del Instituto

### Implementación en `core/validators.py`

La validación de IP se realiza en el backend para seguridad:

```python
# core/validators.py
from django.core.exceptions import PermissionDenied

ALLOWED_IPS = [
    '190.x.x.x',  # IP pública del instituto (reemplazar)
    '127.0.0.1',  # Localhost para desarrollo
]

def validate_institute_ip(request):
    """
    Valida que la petición venga desde la IP del instituto.
    """
    # Obtener IP real (considerando proxies)
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    if ip not in ALLOWED_IPS:
        raise PermissionDenied(
            f"Acceso denegado. Debe conectarse desde la red del instituto."
        )
    
    return True
```

---

## 📦 Dependencias del Proyecto

### requirements.txt

```
# Framework
Django>=5.0
djangorestframework>=3.14.0

# Autenticación JWT
djangorestframework-simplejwt>=5.3.0

# CORS para frontend
django-cors-headers>=4.3.0

# Variables de entorno
python-decouple>=3.8

# Base de datos PostgreSQL
psycopg2-binary>=2.9.11
```

---

## 🔒 Variables de Entorno

El proyecto usa **python-decouple** para manejar configuración sensible mediante archivos `.env`.

### Backend (.env)

```bash
# Django Settings
DEBUG=True                    # False en producción
SECRET_KEY=tu-secret-key      # Generar con: python -c "import secrets; print(secrets.token_urlsafe(50))"
ALLOWED_HOSTS=localhost,127.0.0.1

# Database PostgreSQL
DB_ENGINE=django.db.backends.postgresql
DB_NAME=produs_horas
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# JWT
JWT_ACCESS_TOKEN_LIFETIME_HOURS=8
JWT_REFRESH_TOKEN_LIFETIME_DAYS=7

# IP Validation
ALLOW_ALL_IPS=True            # False en producción
ALLOWED_IPS=127.0.0.1,::1,IP.PUBLICA.INSTITUTO
```

### Frontend (.env)

```bash
# API Backend
VITE_API_BASE_URL=http://localhost:8000/api

# Ambiente
VITE_APP_ENV=development      # production en producción
VITE_APP_NAME=ProDus Registro de Horas
VITE_APP_VERSION=1.0.0
```

### Archivos de Entorno

| Archivo | Propósito | ¿Commitear? |
|---------|-----------|-------------|
| `.env` | Desarrollo local | ❌ No |
| `.env.example` | Plantilla para nuevos devs | ✅ Sí |
| `.env.production` | Referencia para producción | ❌ No |

---

## 🚀 Roadmap de Implementación

### Fase 1: Configuración Base
- [ ] Instalar dependencias
- [ ] Configurar Django REST Framework
- [ ] Configurar JWT
- [ ] Configurar CORS

### Fase 2: Módulo Authentication
- [ ] Crear app `authentication`
- [ ] Implementar validación de IP
- [ ] Endpoints: login, logout, refresh token

### Fase 3: Módulo Employees
- [ ] Crear app `employees`
- [ ] Modelo Employee
- [ ] CRUD de empleados

### Fase 4: Módulo Time Entries
- [ ] Crear app `time_entries`
- [ ] Modelo TimeEntry
- [ ] Endpoints para registro de horas

### Fase 5: Integración Frontend
- [ ] Conectar Vue.js con API
- [ ] Implementar auth en frontend
- [ ] Testing integración

---

## 📚 Referencias

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/)

---

*Documento generado el 3 de febrero de 2026*
*Versión: 1.0*
