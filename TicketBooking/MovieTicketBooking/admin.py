from django.contrib import admin
from .models import Movies,Theater,TotalCount,ShowTiming

admin.register(Movies,Theater,TotalCount,ShowTiming)(admin.ModelAdmin)
# Register your models here.
