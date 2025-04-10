from apps.symptom.views.customers_view import *
from django.urls import path


urlpatterns = [
    path('customers/', customers_view, name='customers_view'),
    path('filter-customers/', filter_customers_view, name='filter_customers_view'),
    path('customer-create/', create_customer_view, name='create_customer_view'),
    path('customer-detail/<int:pk>/', detail_customer_view, name='detail_customer_view'),
    path('customer-upload-file/<int:pk>/', upload_file, name='upload_file'),
    path('customer-update/<int:pk>/', update_customer_view, name='update_customer_view'),
    path('customer-sign/<int:pk>/', sign_customer_view, name='sign_customer_view'),
]
