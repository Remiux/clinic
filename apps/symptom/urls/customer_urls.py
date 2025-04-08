from apps.symptom.views.customers_view import *
from django.urls import path


urlpatterns = [
  
    path('customers/', customers_view, name='customers_view'),
    path('customer-detail/<int:pk>/', detail_customer_view, name='detail_customer_view'),
    path('customer-sign/<int:pk>/', sign_customer_view, name='sign_customer_view'),
    
]
