from django.contrib import admin
from .models import Movie

# Register your models here.

class Movie_Admin(admin.ModelAdmin):
    list_display=['name','protagonists','release_date','status','poster','trailer','rating']

admin.site.register(Movie,Movie_Admin)
