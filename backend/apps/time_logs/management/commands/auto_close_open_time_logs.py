from asgiref.sync import async_to_sync
from django.core.management.base import BaseCommand

from apps.time_logs.services import close_open_time_logs_by_system


class Command(BaseCommand):
    help = "Cierra jornadas abiertas y marca closed_by=SYSTEM con valores default de formulario."

    def handle(self, *args, **options):
        total_closed = async_to_sync(close_open_time_logs_by_system)()

        self.stdout.write(
            self.style.SUCCESS(
                f"Cierre automático completado. Jornadas cerradas por sistema: {total_closed}"
            )
        )
