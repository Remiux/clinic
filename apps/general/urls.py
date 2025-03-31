from apps.general.views import index, test
from django.urls import path, include, re_path


urlpatterns = [
    path('', index, name='index'),
    path('test', test, name='test'),
    path('', include('apps.accounts.urls.users_urls')),
]
