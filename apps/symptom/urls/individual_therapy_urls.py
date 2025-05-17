from apps.symptom.views.successfully_individual_therapy_section_view import *
from apps.symptom.views.individual_therapy_view import *
from apps.symptom.views.therapists_customer_check_section_view import *
from apps.symptom.views.therapists_groups_view import *
from apps.symptom.views.customers_view import *
from django.urls import path


urlpatterns = [
    
    path('individual-therapy/', individual_terapy_view, name='individual_terapy_view'),
    path('individual-therapy-filter/', filter_individual_therapy_view, name='filter_individual_therapy_view'),
    path('individual-therapy-create/', create_individual_therapy_view, name='create_individual_therapy_view'),
    path('individual-therapy-detail/<int:pk>/', detail_individual_therapy_view, name='detail_individual_therapy_view'),
    path('individual-therapy-update-service/<int:pk>/', update_service_individual_therapy_view, name='update_service_individual_therapy_view'),
    path('individual-therapy-update-therapist/<int:pk>/', update_therapist_individual_therapy_view, name='update_therapist_individual_therapy_view'),
    path('individual-therapy-delete-section/<int:pk>/', delete_section_individual_therapy_view, name='delete_section_individual_therapy_view'),
    path('individual-therapy-create-section/<int:pk>/', create_section_individual_therapy_view, name='create_section_individual_therapy_view'),
    path('individual-therapy-update-date-section/<int:pk>/', update_date_individual_therapy_view, name='update_date_individual_therapy_view'),
    path('individual-therapy-confirm-section/<int:pk>/', confirm_section_individual_therapy_view, name='confirm_section_individual_therapy_view'),
    
   # Individual Therapy Section Successfully
    path('individual-therapy-successfully/', successfully_individual_therapy_section_view, name='successfully_individual_therapy_section_view'),
    path('individual-therapy-successfully-filter/', filter_successfully_individual_therapy_section_view, name='filter_successfully_individual_therapy_section_view'),
    path('detail-individual-therapy-successfully/<int:pk>/', detail_successfully_individual_therapy_view, name='detail_successfully_individual_therapy_view'),
    path('add-goal-individual-therapy-successfully/<int:pk>/<int:goal>/', add_goal_individual_therapy_note_view, name='add_goal_individual_therapy_note_view'),
    path('delete-goal-individual-therapy-successfully/<int:pk>/', delete_goal_individual_therapy_note_view, name='delete_goal_individual_therapy_note_view'),
    path('delete-objective-goal-individual-therapy-successfully/<int:pk>/', delete_objective_goal_individual_therapy_note_view, name='delete_objective_goal_individual_therapy_note_view'),
    path('sign-individual-therapy-note/<int:pk>/', sign_individual_note_view, name='sign_individual_note_view'),
    path('update-individual-therapy-note/<int:pk>/', update_individual_therapy_section_view, name='update_individual_therapy_section_view'),
    
    
    
]
