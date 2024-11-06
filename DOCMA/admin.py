from django.contrib import admin
from .models import *
# Register your models here.

admin.register(doc_holder)(admin.ModelAdmin)
admin.register(doc_type)(admin.ModelAdmin)
admin.register(docma)(admin.ModelAdmin)
admin.register(home_menu)(admin.ModelAdmin)
admin.register(docma_firebase)(admin.ModelAdmin)