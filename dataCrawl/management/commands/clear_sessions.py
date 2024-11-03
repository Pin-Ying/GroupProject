from django.core.management.base import BaseCommand
from django.contrib.sessions.models import Session


class Command(BaseCommand):
    help = "Clear all session data"

    def handle(self, *args, **kwargs):
        Session.objects.all().delete()
        self.stdout.write(self.style.SUCCESS("Successfully cleared all sessions"))
