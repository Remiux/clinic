from apps.general.views import index, test,login_view
from django.urls import path, include, re_path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', index, name='index'),
    path('test', test, name='test'),
    path('login', login_view, name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('', include('apps.accounts.urls.users_urls')),
]
