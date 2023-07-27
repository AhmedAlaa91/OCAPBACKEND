# coding: utf-8
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Initialize OCAP default data'

    def handle(self, *args, **options):
        try:
            from django.core.management import execute_from_command_line
            import sys
            self.stdout.write(self.style.NOTICE(
                'Load OCAP data is in progress'))
            execute_from_command_line(
                [sys.argv[0], 'loaddata', 'data.json'],
            )

        except Exception as ex:
            self.stdout.write(self.style.NOTICE(
                f'Error :{str(ex)}'))
