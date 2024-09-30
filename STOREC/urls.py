
from django.urls import path , include
from STOREC import views
from rest_framework_simplejwt.views import TokenObtainPairView
urlpatterns = [
    # path('' , views.dem_dashboard),
    path('' , views.one_percent_analyser),
    path('fileupload/' , views.file_uploader),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
