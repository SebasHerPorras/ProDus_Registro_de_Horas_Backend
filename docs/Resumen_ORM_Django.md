# Resumen: ORM de Django, SQL y arquitectura

## 1) ¿Qué es el ORM de Django?
El ORM (Object-Relational Mapper) permite trabajar con la base de datos usando clases Python (models) en lugar de escribir SQL directamente. Django se encarga de traducir esas operaciones a SQL compatible con PostgreSQL.

**Ventajas**
- Menos errores y más seguridad (reduce riesgo de SQL injection).
- Código más limpio y mantenible.
- Migraciones automáticas para versionar cambios de la base de datos.
- Portabilidad (aunque aquí siempre usamos PostgreSQL).

## 2) ¿Cómo se “nombran” las cosas en SQL desde Django?
En Django, el nombre de tabla se define en el modelo con `db_table`:

```py
class User(models.Model):
    class Meta:
        db_table = 'user'
```

Si no se define `db_table`, Django usa `appname_modelname`.

**Nombres de columnas**
Cada atributo del modelo se convierte en una columna. Por ejemplo:

```py
username = models.CharField(max_length=255)
```

genera una columna `username` en la tabla.

## 3) ¿Cómo se usa el ORM?
Ejemplos básicos:

```py
# Crear
User.objects.create_user(username='juan', password='123')

# Leer
User.objects.get(username='juan')
User.objects.filter(is_active=True)

# Actualizar
User.objects.filter(id=1).update(is_active=False)

# Eliminar
User.objects.filter(id=1).delete()
```

## 4) ¿Cómo se generan cosas nuevas (migraciones)?
Cada vez que cambias un modelo:

1. **Crear migración**
   ```bash
   python manage.py makemigrations
   ```

2. **Aplicar migración**
   ```bash
   python manage.py migrate
   ```

Django guarda estos cambios en archivos dentro de `migrations/` y lleva el historial en la tabla `django_migrations`.

## 5) Arquitectura actual del proyecto (resumen)

### Backend (Django)
- **apps/users**: usuarios, personas y asistentes.
- **apps/authentication_authorization**: rangos IP permitidos (AllowedIPRange).
- **apps/schedules**: horarios.
- **apps/activities**: actividades.
- **apps/reports**: reportes.
- **core/**: permisos, validadores, paginación y excepciones.

**Flujo de IPs**
- El backend valida IPs con `IsFromInstitute`.
- Los rangos permitidos se guardan en DB (AllowedIPRange) y se validan con CIDR.
- En modo desarrollo (`ALLOW_ALL_IPS=True`) se permite todo.

### Frontend (Vue + Vite)
- **router**: usa un guard para bloquear si la IP no es válida.
- **views**: `LoginView`, `HomeView`, `BlockedView`.
- **services/api.ts**: maneja login, refresh y validación de IP.

## 6) ¿Cuándo usar SQL directo?
Solo cuando el ORM no sea suficiente (consultas complejas, reportes especiales). Aun así, el ORM cubre casi todo lo necesario en este sistema.

```py
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM user WHERE is_admin = %s", [True])
    rows = cursor.fetchall()
```

## 7) Recomendación práctica
- Usa el ORM para todo lo normal.
- Cambia modelos y genera migraciones.
- Evita SQL directo salvo necesidad real.
