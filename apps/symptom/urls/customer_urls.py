from apps.symptom.views.customers_view import *
from django.urls import path


urlpatterns = [
    path('customers/', customers_view, name='customers_view'),
    path('filter-customers/', filter_customers_view, name='filter_customers_view'),
    path('filter-files/<int:pk>/', filter_files_view, name='filter_files_view'),
    path('customer-create/', create_customer_view, name='create_customer_view'),
    path('customer-detail/<int:pk>/', detail_customer_view, name='detail_customer_view'),
    path('customer-upload-file/<int:pk>/', upload_file, name='upload_file'),
    path('customer-delete-file/<int:pk>/', delete_file_view, name='delete_file_view'),
    path('customer-delete-elegibility-file/<int:pk>/', delete_elegibility_file_view, name='delete_elegibility_file_view'),
    path('customer-update/<int:pk>/', update_customer_view, name='update_customer_view'),
    path('customer-sign/<int:pk>/', sign_customer_view, name='sign_customer_view'),
    path('customer-delete-psichiatric-evaluation-file/<int:pk>/', delete_psichiatric_evaluation_file_view, name='delete_psichiatric_evaluation_file_view'),
    path('customer-delete-yearly-physical-file/<int:pk>/', delete_yearly_physical_file_view, name='delete_yearly_physical_file_view'),
    path('customer-delete-suicidal-risk-file/<int:pk>/', delete_suicide_risk_file_view, name='delete_suicide_risk_file_view'),
    path('customer-delete-behavioral-health-file/<int:pk>/', delete_behavioral_health_file_view, name='delete_behavioral_health_file_view'),
    path('customer-delete-bio-psycho-social-assessments-file/<int:pk>/', delete_bio_psycho_social_assessments_file_view, name='delete_bio_psycho_social_assessments_file_view'),
    path('customer-delete-brief-behavioral-health-file/<int:pk>/', delete_brief_behavioral_health_file_view, name='delete_brief_behavioral_health_file_view'),
    path('customer-delete-discharge-summary-file/<int:pk>/', delete_discharge_summary_file_view, name='delete_discharge_summary_file_view'),
    path('customer-delete-far-file/<int:pk>/', delete_far_file_view, name='delete_far_file_view'),
    
    
]
