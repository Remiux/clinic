from django.urls import path
from apps.symptom.views.cryptography_view import upload_file, list_files, download_file

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    path('list/', list_files, name='list_files'),
    path('download/<int:file_id>/', download_file, name='download_file'),
]