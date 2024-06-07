from django.urls import path , include
from MEDTRAC import views
urlpatterns = [
    path('' , views.medtrac_dashboard),
    path('log_medtrac/',views.log_medtrac)
]
