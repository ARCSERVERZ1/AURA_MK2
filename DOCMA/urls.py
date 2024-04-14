
from django.contrib import admin
from django.urls import path , include
from DOCMA import views as v


urlpatterns = [
        path('' , v.doc_manger_home ),
        path('add_doc/' , v.add_document ),
        path('save/' , v.doc_manager_save ),
        path('test/' , v.test ),
        path('doc_viewer/<str:type>/' , v.doc_viewer )
]