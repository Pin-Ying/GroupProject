# your_app/management/commands/upload_data.py

from django.core.management.base import BaseCommand
from dataCrawl import dbUpdate
from dataCrawl import comments

class Command(BaseCommand):
    help = 'Upload data to multiple models using bulk_create'

    def add_arguments(self, parser):
        parser.add_argument(
            '--model', 
            type=str, 
            choices=['theaters', 'movies', 'shows','comments'], 
            help='Specify which model to update'
        )


    def handle(self, *args, **kwargs):
        model = kwargs['model']
        self.stdout.write('Data uploading...')

        if model == 'theaters':
            self.stdout.write('UpdateTheater START...')
            dbUpdate.UpdateTheater(mode='csv')
            self.stdout.write('UpdateTheater FINISH')
        
        elif model == 'movies':
            self.stdout.write('UpdateMovies START...')
            dbUpdate.UpdateMovies()
            self.stdout.write('UpdateMovies FINISH')
        
        elif model == 'shows':
            self.stdout.write('UpdateShows START...')
            dbUpdate.UpdateShows()  # 假設你已經定義了這個函數
            self.stdout.write('UpdateShows FINISH')
        
        elif model == 'comments':
            self.stdout.write('import_reviews START...')
            comments.import_reviews()
            self.stdout.write('import_reviews FINISH')

        self.stdout.write(self.style.SUCCESS('Data uploaded successfully'))


