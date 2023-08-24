# coding: utf-8
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            import sys

            from django.core.management import execute_from_command_line

            self.stdout.write(self.style.NOTICE("Load OCAP data is in progress"))
            execute_from_command_line(
                [sys.argv[0], "loaddata", "data.json"],
            )

        except Exception as ex:
            self.stdout.write(self.style.NOTICE(f"Error :{str(ex)}"))
