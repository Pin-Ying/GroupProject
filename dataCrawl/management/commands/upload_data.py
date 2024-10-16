# your_app/management/commands/upload_data.py

from django.core.management.base import BaseCommand
from dataCrawl import dbUpdate

class Command(BaseCommand):
    help = 'Upload data to multiple models using bulk_create'


    def handle(self, *args, **kwargs):
        self.stdout.write('Data uploading...')

        # self.stdout.write('UpdateTheater START...')
        # dbUpdate.UpdateTheater()
        # self.stdout.write('UpdateTheater FINISH')
        self.stdout.write('UpdateMovies START...')
        dbUpdate.UpdateMovies()
        self.stdout.write('UpdateMovies FINISH')
        self.stdout.write(self.style.SUCCESS('Data uploaded to ModelA successfully'))


