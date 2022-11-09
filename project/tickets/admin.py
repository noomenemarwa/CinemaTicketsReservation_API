from django.contrib import admin
from .models import Movie, Guest, Resevation


admin.site.register(Movie)
admin.site.register(Resevation)
admin.site.register(Guest)
