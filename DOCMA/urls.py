
from django.contrib import admin
from django.urls import path , include
from DOCMA import views as v
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
        path('' , v.doc_manger_home ),
        path('add_doc/' , v.add_document ),
        path('save/' , v.doc_manager_save_firebase ),
        path('test/' , v.test ),
        path('add_new_type/<str:new_doc_type>/' , v.add_doc_type ),
        path('get_data_by_id/<str:id>/' , v.get_data_by_id_firebase ),
        path('delete_data_by_id/<str:id>/' , v.delete_data_by_id ),
        path('save_edit_document/' , v.add_edit_document_firebase ),
        path('doc_viewer/<str:type>/' , v.doc_viewer_firebase ),
        path('rag_data' , v.rag_for_docma ),
        path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]