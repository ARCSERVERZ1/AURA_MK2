from django.contrib import admin
from .models import *
# Register your models here.


admin.register(locations_data)(admin.ModelAdmin)