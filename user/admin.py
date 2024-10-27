from django.contrib import admin
from .models import Movie, Review, User, Click

# Register your models here.
admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(User)
admin.site.register(Click)