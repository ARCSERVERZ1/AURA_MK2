from django.urls import path , include
from GENERAL_APPS import views
urlpatterns = [
    path('get_loc/',views.form_save_loc),
    path('save_loc/',views.save_loc),

]
