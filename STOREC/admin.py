from django.contrib import admin
from STOREC.models import *
# Register your models here.



admin.register(stock_list)(admin.ModelAdmin)