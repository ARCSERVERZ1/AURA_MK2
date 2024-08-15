"""
URL configuration for AURA_MK2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home_styles, name='home_styles')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home_styles')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from AURA_MK2 import views as v
urlpatterns = [
    path('admin/', admin.site.urls),
    path('dem/' , include('DEM.urls')),
    path('doc_manager/' , include('DOCMA.urls')),
    path('medtrac/' , include('MEDTRAC.urls')),
    path('' , v.login ),
    path('home/' , v.home_page ),
    path('homeautom/' , include('HOMEAUTOM.urls') ),
    path('storec/' , include('STOREC.urls') ),

]
