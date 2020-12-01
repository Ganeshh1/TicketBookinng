from django.contrib import admin
from .models import Movies,Theater,ShowTiming

admin.register(Movies,Theater,ShowTiming)(admin.ModelAdmin)
# Register your models here.
