from apps.accounts.views.users_view import users_view
from django.urls import path


urlpatterns = [
    path('users', users_view, name='users_view'),
]
