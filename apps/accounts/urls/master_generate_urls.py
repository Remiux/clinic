from apps.accounts.views.master_generate import *
from django.urls import path


urlpatterns = [
    path('generate-masters/<int:pk>/', generate_master_view, name='generate_master_view'),
    path('filter-generate-master/<int:pk>/', filter_generate_master_view, name='filter_generate_master_view'),
    path('create-generate-masters/<int:pk>/', create_generate_master_view, name='create_generate_master_view'),
    path('delete-generate-masters/<int:pk>/', delete_generate_master_view, name='delete_generate_master_view'),
   
]
