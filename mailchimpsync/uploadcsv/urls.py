from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload_csv, name='upload_csv'),
    path('connection-check', views.connection_check, name='connection_check'),
    path('success', views.success, name='success'),
    path('error', views.error, name='error'),
    path('download', views.list_download, name='list_download'),
    path('list-download-csv/', views.download_list, name='download_list')
]