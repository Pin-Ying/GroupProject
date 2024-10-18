from django.contrib import admin
from search.models import movie, theater, showTimeInfo, Review

# Register your models here.
admin.site.register(movie)
admin.site.register(theater)
admin.site.register(showTimeInfo)
admin.site.register(Review)
