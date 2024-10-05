from django.urls import path , include
from GENERAL_APPS import views
urlpatterns = [
    path('location/home',views.form_save_loc, name = 'location_home'),
    path('location/save_loc',views.save_loc),

]
