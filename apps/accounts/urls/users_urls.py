from apps.accounts.views.users_view import users_view,update_user_view,detail_user_view,filter_users_view,create_user_view,user_profile_view,change_password_view, upload_file_user, filter_files_user_view, delete_file_user_view
from django.urls import path


urlpatterns = [
    path('users/', users_view, name='users_view'),
    path('filter-users', filter_users_view, name='filter_users_view'),
    path('filter-files-user/<int:pk>/', filter_files_user_view, name='filter_files_user_view'),
    path('users-create/', create_user_view, name='create_user_view'),
    path('users-detail/<int:pk>/', detail_user_view, name='detail_user_view'),
    path('users-update/<int:pk>/', update_user_view, name='update_user_view'),
    path('change-password/', change_password_view, name='change_password_view'),
    path('my-profile/', user_profile_view, name='user_profile_view'),
    path('user-upload-file/<int:pk>/', upload_file_user, name='upload_file_user'),
    path('customer-delete-file-user/<int:pk>/', delete_file_user_view, name='delete_file_user_view'),
    
    
    
]
