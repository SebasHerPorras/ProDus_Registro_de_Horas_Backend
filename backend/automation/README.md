# Automation Runner

Esta carpeta permite ejecutar funciones automáticas del backend de manera controlada.

Cuando un job está `ENABLED`, este runner lo registra en `crontab` con su horario específico.

## Estructura

- `jobs/`: scripts de trabajos automáticos (`*.bash` o `*.sh`).
- `schedules/`: horario por job (`<job_name>.cron`, expresión de 5 campos).
- `enabled/`: banderas (`*.enabled`) para saber qué jobs están activos.
- `logs/`: bitácora de activaciones y ejecuciones.
- `run_job.bash`: ejecuta un job específico.
- `run_enabled.bash`: ejecuta todos los jobs habilitados.
- `enable_job.bash`: habilita un job o todos.
- `disable_job.bash`: deshabilita un job o todos.
- `list_jobs.bash`: muestra estado ENABLED/DISABLED.
- `set_schedule.bash`: define/actualiza horario cron de un job.

## Uso rápido

Desde `backend/automation`:

```bash
./list_jobs.bash
./set_schedule.bash close_open_time_logs "0 0 * * *"
./enable_job.bash close_open_time_logs
./run_job.bash close_open_time_logs
./run_enabled.bash
./disable_job.bash close_open_time_logs
./enable_job.bash --all
./disable_job.bash --all
```

## Horarios por job

Cada job usa su archivo en `schedules/`:

- `schedules/close_open_time_logs.cron` -> `0 0 * * *` (medianoche)

Ejemplo para miércoles a las 7:00 am:

```bash
./set_schedule.bash close_open_time_logs "0 7 * * 3"
```

## ¿Cómo se ejecuta automáticamente?

Al hacer `enable_job`, el script crea/actualiza una entrada en `crontab` para ese job.

Al hacer `disable_job`, el script elimina la entrada cron de ese job.

`run_job` y `run_enabled` siguen existiendo para ejecuciones manuales inmediatas.

## Cron (alternativa global)

Ejecutar jobs habilitados todos los días a las 00:00:

```cron
0 0 * * * cd /home/sebas-uwu/Desktop/Produs/ProDus_Registro_de_Horas_Backend/backend/automation && ./run_enabled.bash
```

## Logging

- Log general: `logs/automation.log`
- Log por job: `logs/<job_name>.log`
