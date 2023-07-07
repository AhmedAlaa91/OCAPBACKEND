# coding: utf-8
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Initialize default data'

    def handle(self, *args, **options):
        # User Groups Check and Create
        if Group.objects.count() == 0:
            self.stdout.write(self.style.NOTICE(
                'Populate default groups in database'))
            Group.objects.get_or_create(name='Admin')
            Group.objects.get_or_create(name='Driver')
            Group.objects.get_or_create(name='Rider')
        if User.objects.count() == 0:
            self.stdout.write(self.style.NOTICE(
                'User database is empty, creating a default superuser: admin / Orange000'))
            User.objects.create_superuser(
                'admin', 'noreply.admin@orange.com', 'Orange000')
