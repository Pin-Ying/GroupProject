# your_app/management/commands/upload_data.py

from django.core.management.base import BaseCommand
from dataCrawl import dbUpdate

class Command(BaseCommand):
    help = 'Upload data to multiple models using bulk_create'


    def handle(self, *args, **kwargs):
        self.stdout.write('Data uploading...')

        dbUpdate.UpdateMovies()
        self.stdout.write(self.style.SUCCESS('Data uploaded to ModelA successfully'))

