# Ejemplo: App Django "departments" solo base de datos

## 1. ¿Cuándo crear una app?
- Cuando tienes una funcionalidad o dominio de negocio claro (usuarios, reportes, actividades, departamentos, etc).
- Cada app es un módulo independiente y puede tener modelos, lógica de negocio, endpoints, etc.

## 2. ¿Cuándo solo crear una tabla sin lógica de negocio?
- Cuando solo necesitas almacenar información simple (catálogos, listas, configuraciones) y no hay reglas ni procesos asociados.
- Ejemplo: actividades, departamentos, tipos de documento, países, etc.
- No necesitas crear views, serializers, services ni urls si no vas a exponer la tabla por API ni necesitas lógica adicional.

---

## 3. Ejemplo completo: App "departments"

### a) Crear la app
```bash
python manage.py startapp departments
```

### b) Definir el modelo en departments/models.py
```python
from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
```

### c) Registrar la app en settings.py
Agrega `'apps.departments',` en la lista `INSTALLED_APPS`.

### d) Crear migración y aplicarla
```bash
python manage.py makemigrations departments
python manage.py migrate
```

### e) (Opcional) Registrar en admin.py
```python
from django.contrib import admin
from .models import Department

admin.site.register(Department)
```

---

## 4. Estructura interna recomendada para una app Django

- models.py: Definición de entidades/tablas
- admin.py: Configuración para el panel de administración
- views.py: Endpoints/controladores (solo si hay API)
- serializers.py: Transformación de datos (solo si hay API)
- services.py: Lógica de negocio (solo si hay reglas/procesos)
- urls.py: Rutas (solo si hay API)
- tests.py: Pruebas

---

## 5. Resumen
- Si solo necesitas la tabla, define el modelo en models.py y registra la app en INSTALLED_APPS.
- Si en el futuro necesitas lógica o endpoints, puedes agregar los archivos correspondientes.
- Así mantienes la estructura limpia y simple.