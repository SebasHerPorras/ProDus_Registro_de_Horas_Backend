# Automation Runner

Esta carpeta permite ejecutar funciones automáticas del backend de manera controlada.

Cuando un job está `ENABLED`, este runner lo registra en `crontab` con su horario específico.

## Estructura

- `jobs/`: scripts de trabajos automáticos (`*.bash` o `*.sh`).
- `schedules/`: horario por job (`<job_name>.cron`, expresión de 5 campos cron).
- `enabled/`: banderas (`*.enabled`) para saber qué jobs están activos.
- `logs/`: bitácora de activaciones y ejecuciones.

## Scripts de Control

### `run_job.bash`

**Función**: Ejecuta un job específico manualmente.

**Uso**:

```bash
./run_job.bash close_open_time_logs
./run_job.bash close_open_time_logs.bash  # también funciona
```

**Qué hace**:
- Resuelve el nombre del job automáticamente (con o sin extensión `.bash` o `.sh`)
- Ejecuta el script del job desde la carpeta `jobs/`
- Registra la ejecución en `logs/{job_name}.log`
- Retorna código de salida 0 si tiene éxito, 1 si falla

---

### `run_enabled.bash`
**Función**: Ejecuta TODOS los jobs que están actualmente habilitados (marcados con `.enabled`).

**Uso**:
```bash
./run_enabled.bash
```

**Qué hace**:
- Busca todos los archivos `.enabled` en la carpeta `enabled/`
- Por cada job habilitado, llama a `run_job.bash` para ejecutarlo
- Si no hay jobs habilitados, sale silenciosamente
- Reporta total de jobs ejecutados y cantidad de fallos
- Retorna 1 si al menos un job falló, 0 si todos tuvieron éxito
- Ideal para ejecutar periódicamente desde cron

---

### `enable_job.bash`
**Función**: Habilita un job o todos, y lo registra en `crontab` con su horario.

**Uso**:
```bash
./enable_job.bash close_open_time_logs
./enable_job.bash --all  # habilita todos los jobs
```

**Qué hace**:

- Crea un archivo `.enabled` en la carpeta `enabled/`
- Lee el horario cron desde `schedules/{job_name}.cron`
- Valida que el horario tenga exactamente 5 campos
- Agrega una entrada en `crontab` que ejecutará `run_job.bash` con ese horario
- Usa un marcador automático (`AUTO_JOB:`) para identificar y no duplicar entradas
- Registra la acción en el log

**Requisito previo**: El archivo `schedules/{job_name}.cron` debe existir con un horario válido.

---

### `disable_job.bash`

**Función**: Deshabilita un job o todos, eliminándolo de `crontab`.

**Uso**:

```bash
./disable_job.bash close_open_time_logs
./disable_job.bash --all  # deshabilita todos los jobs
```

**Qué hace**:

- Elimina el archivo `.enabled` de la carpeta `enabled/`
- Busca y elimina la entrada cron correspondiente del `crontab`
- Usa el marcador automático para identificar la entrada correcta
- Registra la acción en el log
- El job sigue siendo ejecutable manualmente con `run_job.bash`

---

### `list_jobs.bash`

**Función**: Muestra el estado actual (ENABLED/DISABLED) de todos los jobs.

**Uso**:

```bash
./list_jobs.bash
```

**Qué hace**:

- Lista todos los scripts disponibles en `jobs/`
- Para cada job, indica si tiene o no un archivo `.enabled`
- Muestra el horario cron desde `schedules/{job_name}.cron`
- Útil para ver el estado general del sistema de automatización

---

### `set_schedule.bash`

**Función**: Define o actualiza el horario cron para un job.

**Uso**:

```bash
./set_schedule.bash close_open_time_logs "0 0 * * *"
./set_schedule.bash close_open_time_logs "0 7 * * 3"  # miércoles a las 7:00 AM
```

**Qué hace**:
- Crea o sobrescribe el archivo `schedules/{job_name}.cron` con la expresión cron proporcionada
- Valida que la expresión tenga exactamente 5 campos
- Si el job está habilitado, actualiza automáticamente la entrada en `crontab`
- Registra la acción en el log

**Formato cron** (5 campos):
```
┌───────────── Minuto (0-59)
│ ┌───────────── Hora (0-23)
│ │ ┌───────────── Día del mes (1-31)
│ │ │ ┌───────────── Mes (1-12)
│ │ │ │ ┌───────────── Día de la semana (0-6, donde 0=domingo)
│ │ │ │ │
│ │ │ │ │
* * * * *
```

---

## Jobs Disponibles

### `close_open_time_logs.bash`
**Función**: Cierra automáticamente los registros de tiempo que permanecen abiertos.

**Ubicación**: `jobs/close_open_time_logs.bash`

**Qué hace**:
- Ejecuta el comando Django: `python manage.py auto_close_open_time_logs`
- Busca en la base de datos todos los registros de tiempo (`TimeLogs`) que no tienen hora de cierre (`end_time`)
- Cierra automáticamente los que cumplen ciertos criterios (por ejemplo, que llevan más de X horas abiertos)
- Registra la acción en el log

**Horario recomendado**: Medianoche (`0 0 * * *`), o el momento que mejor se adapte a tu negocio.

---

## Ejemplos de Uso

### Flujo típico: Habilitar y automatizar un job

```bash
# 1. Ver todos los jobs disponibles
./list_jobs.bash

# 2. Establecer el horario (medianoche todos los días)
./set_schedule.bash close_open_time_logs "0 0 * * *"

# 3. Habilitar el job (se agrega a crontab)
./enable_job.bash close_open_time_logs

# 4. Verificar que fue habilitado
./list_jobs.bash

# 5. Ejecutar manualmente si lo deseas
./run_job.bash close_open_time_logs
```

### Ejecutar todos los jobs habilitados manualmente

```bash
./run_enabled.bash
```

### Cambiar horario de un job ya habilitado

```bash
# Cambiar a las 7:00 AM (todos los días)
./set_schedule.bash close_open_time_logs "0 7 * * *"

# Si el job está habilitado, crontab se actualiza automáticamente
./list_jobs.bash
```

### Deshabilitar temporalmente un job

```bash
./disable_job.bash close_open_time_logs

# Para volver a habilitar:
./enable_job.bash close_open_time_logs
```

### Habilitar/deshabilitar todos los jobs

```bash
./enable_job.bash --all
./disable_job.bash --all
```

---

## Horarios Cron Comunes

| Descripción | Expresión |
|---|---|
| Medianoche todos los días | `0 0 * * *` |
| 7:00 AM todos los días | `0 7 * * *` |
| Miércoles a las 7:00 AM | `0 7 * * 3` |
| Cada hora | `0 * * * *` |
| Cada 30 minutos | `*/30 * * * *` |
| Lunes a viernes a las 9:00 AM | `0 9 * * 1-5` |
| Primer día del mes a medianoche | `0 0 1 * *` |

Para más información sobre cron: [crontab guru](https://crontab.guru/)

---

## ¿Cómo funciona la automatización?

### Flujo de ejecución automática

1. **Cuando haces `enable_job`**:
   - Se crea un archivo `.enabled` en la carpeta `enabled/`
   - Se lee el horario desde `schedules/{job_name}.cron`
   - Se agrega una entrada a `crontab` que ejecutará el job en el horario especificado

2. **En el horario especificado**:
   - El sistema operativo ejecuta el comando registrado en `crontab`
   - Se llama a `run_job.bash` con el nombre del job
   - El job se ejecuta y sus resultados se registran en el log

3. **Cuando haces `disable_job`**:
   - Se elimina el archivo `.enabled`
   - Se elimina la entrada del `crontab`
   - El job ya no se ejecutará automáticamente (pero puedes seguir ejecutándolo manualmente)

### Ver y editar crontab directamente

Para ver todas las entradas de cron activas:
```bash
crontab -l
```

Para editar manualmente:
```bash
crontab -e
```

**Nota**: Los jobs habilitados mediante `enable_job.bash` tienen un marcador `# AUTO_JOB:` que facilita su identificación y evita duplicados.

---

## Sistema de Logging

El sistema registra todas las actividades en archivos de log:

### Ubicación de logs

```
logs/
  ├── automation.log              # Log general de todas las acciones
  ├── close_open_time_logs.log    # Log específico del job
  └── cron.log                    # Salida de ejecuciones desde crontab
```

### Contenido de los logs

**`automation.log`** - Eventos de habilitación, deshabilitación y ejecución:
```
[2026-04-29 14:30:00+0000] ENABLE job=close_open_time_logs.bash schedule='0 0 * * *'
[2026-04-29 14:30:05+0000] RUN_ENABLED END total=1 failed=0
```

**logs job específico** - Salida detallada de la ejecución:
```
[2026-04-29 00:00:01+0000] START JOB=close_open_time_logs
Closed N logs
[2026-04-29 00:00:05+0000] END JOB=close_open_time_logs status=ok
```

### Ver logs en tiempo real

```bash
# Ver log general
tail -f logs/automation.log

# Ver log específico de un job
tail -f logs/close_open_time_logs.log

# Ver últimos 20 líneas
tail -n 20 logs/automation.log
```

---

## Troubleshooting y Mejores Prácticas

### El job no se ejecuta a la hora especificada

1. **Verifica que el job esté habilitado**:
   ```bash
   ./list_jobs.bash
   ```
   Deberías ver el estado "ENABLED" para el job.

2. **Verifica que crontab tiene la entrada**:
   ```bash
   crontab -l | grep AUTO_JOB
   ```

3. **Revisa los logs**:
   ```bash
   tail -f logs/cron.log
   tail -f logs/automation.log
   ```

4. **Prueba ejecutar manualmente**:
   ```bash
   ./run_job.bash close_open_time_logs
   ```
   Si falla manualmente, hay un problema con el job mismo, no con la automatización.

### El job da error cuando se ejecuta automáticamente

- Revisa `logs/{job_name}.log` para ver el error detallado
- Puede ser un problema de permisos, variables de entorno o rutas
- Prueba ejecutándolo manualmente desde la carpeta `automation/` para reproducir el error

### Cambiar el horario de un job

No necesitas deshabilitar/habilitar. Simplemente:
```bash
./set_schedule.bash close_open_time_logs "0 9 * * *"  # Nueva hora
```

Si el job está habilitado, `crontab` se actualiza automáticamente.

### El comando da error: "No hay horario para..."

Significa que el archivo `schedules/{job_name}.cron` no existe. Solución:
```bash
./set_schedule.bash close_open_time_logs "0 0 * * *"
```

---

## Mejores Prácticas

✅ **Recomendado**:
- Usa `./run_enabled.bash` desde un cron principal si quieres ejecutar todos tus jobs
- Revisa logs regularmente para detectar problemas
- Usa horarios que no se solapen si los jobs consumen muchos recursos
- Sé conservador con la frecuencia de ejecución
- Documenta el propósito de cada job en un comentario en su archivo

❌ **Evitar**:
- Ejecutar jobs con lógica pesada muy frecuentemente (cada minuto)
- Editar `crontab -e` directamente si usas este sistema (usa `enable_job`/`disable_job`)
- Olvidar crear el archivo horario antes de habilitar un job
- Ejecutar múltiples instantancias del mismo job simultáneamente
