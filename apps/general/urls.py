from apps.general.views import index
from django.urls import path, include, re_path


urlpatterns = [
    path('', index, name='index'),
    path('', include('apps.accounts.urls.users_urls')),
]
