from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Executa migrations protegidas por advisory lock PostgreSQL quando disponível.'

    def handle(self, *args, **options):
        if connection.vendor != 'postgresql':
            call_command('migrate', interactive=False)
            return
        with connection.cursor() as cursor:
            cursor.execute('SELECT pg_advisory_lock(7242026)')
            try:
                call_command('migrate', interactive=False)
            finally:
                cursor.execute('SELECT pg_advisory_unlock(7242026)')
