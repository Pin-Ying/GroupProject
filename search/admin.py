from django.contrib import admin
from search.models import movie,theater,showTimeInfo

# Register your models here.
admin.site.register(movie)
admin.site.register(theater)
admin.site.register(showTimeInfo)
