from django.contrib import admin
from .models import movie, theater, showTimeInfo, Review, User, Click

# Register your models here.
admin.site.register(movie)
admin.site.register(theater)
admin.site.register(showTimeInfo)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(Click)