"""
add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from DEM import views
urlpatterns = [
    path('' , views.dem_dashboard),
    path('datalogdem/<int:count>/<str:user>/<str:date>' , views.datalog_transaction_table),
    path('graph/<str:group_type>', views.plot_graph),
    path('submit_groupdata/', views.update_group),
    path('run_datalog/<str:sdate>/<str:edate>/', views.run_datalog),
    path('delete/<str:id>/', views.delete_log),
    path('multiple_edit/<str:data>/<path:ids>/', views.multiple_edit),
    path('add_new_transaction/', views.add_new_transaction),
    path('non_cat/', views.non_cat_trans),
    path('get_data_by_id/<str:id>/', views.get_data_by_id)
]
