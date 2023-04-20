from django.urls import path
from . import views

urlpatterns = [
    path('upload', views.upload_csv, name='upload_csv'),
    path('connection-check', views.connection_check, name='connection_check'),
    path('success', views.success, name='success'),
    path('upload-error', views.upload_error, name='upload_error')
]