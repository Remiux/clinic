from apps.accounts.views.users_view import users_view,update_user_view,detail_user_view,filter_users_view,create_user_view
from django.urls import path


urlpatterns = [
    path('users', users_view, name='users_view'),
    path('filter-users', filter_users_view, name='filter_users_view'),
    path('users-create/', create_user_view, name='create_user_view'),
    path('users-detail/<int:pk>/', detail_user_view, name='detail_user_view'),
    path('users-update/<int:pk>/', update_user_view, name='update_user_view'),
]
