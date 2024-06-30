from django.urls import path , include
from HOMEAUTOM import views as hautom


urlpatterns = [
        path('' , hautom.dashboard),

]