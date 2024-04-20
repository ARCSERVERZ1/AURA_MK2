from django.contrib import admin
from DEM.models import *
# Register your models here.


admin.register(transactions_data)(admin.ModelAdmin)
admin.register(groupdata)(admin.ModelAdmin)
admin.register(category)(admin.ModelAdmin)

