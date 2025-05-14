from apps.symptom.views.successfully_individual_therapy_section_view import *
from apps.symptom.views.individual_therapy_view import *
from apps.symptom.views.therapists_customer_check_section_view import *
from apps.symptom.views.therapists_groups_view import *
from apps.symptom.views.customers_view import *
from django.urls import path


urlpatterns = [
    
    path('individual-terapy/', individual_terapy_view, name='individual_terapy_view'),
    path('individual-terapy-filter/', filter_individual_therapy_view, name='filter_individual_therapy_view'),
    path('individual-terapy-create/', create_individual_therapy_view, name='create_individual_therapy_view'),
    path('individual-terapy-detail/<int:pk>/', detail_individual_therapy_view, name='detail_individual_therapy_view'),
    path('individual-terapy-update-service/<int:pk>/', update_service_individual_therapy_view, name='update_service_individual_therapy_view'),
    path('individual-terapy-update-therapist/<int:pk>/', update_therapist_individual_therapy_view, name='update_therapist_individual_therapy_view'),
    path('individual-terapy-delete-section/<int:pk>/', delete_section_individual_therapy_view, name='delete_section_individual_therapy_view'),
    path('individual-terapy-create-section/<int:pk>/', create_section_individual_therapy_view, name='create_section_individual_therapy_view'),
    path('individual-terapy-update-date-section/<int:pk>/', update_date_individual_therapy_view, name='update_date_individual_therapy_view'),
    path('individual-terapy-confirm-section/<int:pk>/', confirm_section_individual_therapy_view, name='confirm_section_individual_therapy_view'),
    
   # Individual Therapy Section Successfully
    path('individual-terapy-successfully/', successfully_individual_therapy_section_view, name='successfully_individual_therapy_section_view'),
    path('individual-terapy-successfully-filter/', filter_successfully_individual_therapy_section_view, name='filter_successfully_individual_therapy_section_view'),
    
    
]
