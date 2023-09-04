# coding: utf-8
from django.contrib.auth.models import Group, User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Initialize default data"

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            self.stdout.write(
                self.style.NOTICE("User database is empty, creating a default superuser: admin / Orange000")
            )
            User.objects.create_superuser("admin", "noreply.admin@orange.com", "Orange000")
