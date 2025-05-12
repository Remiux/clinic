from apps.symptom.views.individual_therapy_view import *
from apps.symptom.views.therapists_customer_check_section_view import *
from apps.symptom.views.therapists_groups_view import *
from apps.symptom.views.customers_view import *
from django.urls import path


urlpatterns = [
    path('groups/', therapists_groups_view, name='therapists_groups_view'),
    path('groups-filter/', filter_therapists_groups_view, name='filter_therapists_groups_view'),
    path('groups-create/', create_group_view, name='create_group_view'),
    path('group-detail/<int:pk>/', detail_therapists_groups_view, name='detail_therapists_groups_view'),
    path('group-update-therapist-detail/<int:pk>/', update_therapist_group_view, name='update_therapist_group_view'),
    path('group-update-service-detail/<int:pk>/', update_service_group_view, name='update_service_group_view'),
    path('group-customer-delete/<int:pk>/', delete_customer_group_view, name='delete_customer_group_view'),
    path('group-customer-create/<int:pk>/', create_customer_group_view, name='create_customer_group_view'),
    path('group-customer-active-update/<int:pk>/', update_active_service_group_view, name='update_active_service_group_view'),
    # Therapists Customer Check
    path('therapists-customer-check-section/<int:pk>/', therapists_customer_check_view, name='therapists_customer_check_view'),
    path('therapists-customer-checked-assist-section/<int:pk>/', therapists_customer_checked_assist_view, name='therapists_customer_checked_assist_view'),
    path('therapists-customer-checked-all-assist-section/<int:pk>/', therapists_customer_checked_all_assist_view, name='therapists_customer_checked_all_assist_view'),
    path('therapists-customer-unchecked-all-assist-section/<int:pk>/', therapists_customer_unchecked_all_assist_view, name='therapists_customer_unchecked_all_assist_view'),
    path('therapists-add-customer-assist-section/<int:pk>/', therapists_add_customer_assist_view, name='therapists_add_customer_assist_view'),
    path('therapists-customer-remove-assist-list-section/<int:pk>/', therapists_customer_remove_assist_list_view, name='therapists_customer_remove_assist_list_view'),
    path('therapists-confirm-assist-section/<int:pk>/', therapists_confirm_assist_view, name='therapists_confirm_assist_view'),
    # Therapists PSR Sections
    path('therapists-psr-sections/', therapists_sections_groups_view, name='therapists_sections_groups_view'),
    # path('therapist-psr-notes-create/<int:pk>/', create_psr_notes_view, name='create_psr_notes_view'),
    # path('therapist-update-psr-notes/<int:pk>/', update_psr_notes_view, name='update_psr_notes_view'),
    path('therapist-update-psr-notes/<int:pk>/<str:date>/', update_psr_notes_view, name='update_psr_notes_view'),
    
]
