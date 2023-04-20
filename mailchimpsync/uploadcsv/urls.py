from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_csv, name='upload_csv'),
    path('connection-check', views.connection_check, name='connection_check')
]