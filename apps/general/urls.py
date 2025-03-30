from apps.general.views import index
from django.urls import path, include, re_path


urlpatterns = [
    path('', index, name='index'),
]
