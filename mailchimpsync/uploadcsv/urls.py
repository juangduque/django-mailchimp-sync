from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.upload_csv, name='upload_csv'),
    path('connection-check', views.connection_check, name='connection_check'),
    path('download', views.list_download, name='list_download'),
    path('list-download-csv/', views.download_list, name='download_list'),
    path('success', views.success, name='success'),
    path('error', views.error, name='error'),
    path('file-error', views.file_format_error, name='file_format_error'),
]