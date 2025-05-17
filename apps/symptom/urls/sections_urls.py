from apps.symptom.views.insurance_view import *
from django.urls import path

from apps.symptom.views.sections.section1 import *
from apps.symptom.views.sections.section2 import *
from apps.symptom.views.sections.section3 import *
from apps.symptom.views.sections.section4 import *
from apps.symptom.views.sections.section5 import *


urlpatterns = [
    # Section 1
    path('customer-section_one/<int:pk>/', section_one_view, name='section_one_view'),
    path('customer-section_one-export-pdf/<int:pk>/', section_one_document_one_export_pdf, name='section_one_document_one_export_pdf'),
    path('customer-section_one-history/<int:pk>/', section_one_document_one_history, name='section_one_document_one_history'),
    
    # Section 2
    path('customer-section_two/<int:pk>/', section_two_view, name='section_two_view'), 
    path('customer-section_two-history/<int:pk>/', section_two_document_two_history, name='section_two_document_two_history'),
      
    # Section 3
    path('customer-section_three/<int:pk>/', section_three_view, name='section_three_view'),
    path('customer-section_three-history/<int:pk>/', section_three_document_three_history, name='section_three_document_three_history'),
    path('customer-section_three-history2/<int:pk>/', section_three_document_three_history2, name='section_three_document_three_history2'),
    
    # Section 4
    path('customer-section_four/<int:pk>/', section_four_view, name='section_four_view'),
    path('customer-section_four-history-suicide-risk/<int:pk>/', section_four_document_suicida_risk_history, name='section_four_document_suicida_risk_history'),
    path('customer-section_four-history-behavioral-health/<int:pk>/', section_four_document_behavioral_health_history, name='section_four_document_behavioral_health_history'),
    path('customer-section_four-history-bio-psycho-social/<int:pk>/', section_four_document_bio_psycho_social_history, name='section_four_document_bio_psycho_social_history'),
    path('customer-section_four-history-brief-behavioral-health/<int:pk>/', section_four_document_brief_behavioral_health_history, name='section_four_document_brief_behavioral_health_history'),
    path('customer-section_four-history-discharge-summary/<int:pk>/', section_four_document_discharge_summary_history, name='section_four_document_discharge_summary_history'),
    path('customer-section_four-reload-data/<int:pk>/', reload_data, name='reload_data'),
    path('customer-section_four-update-treatment-duration/<int:pk>/', update_treatment_duration, name='update_treatment_duration'),
    path('update-master-psr-section/<int:pk>/', update_psr_master_view, name='update_psr_master_view'),
    path('update-master-individual-therapy-section/<int:pk>/', update_individual_therapy_master_view, name='update_individual_therapy_master_view'),
    path('update-master-initial-discharge-criteria-section/<int:pk>/', update_initial_discharge_criteria_master_view, name='update_initial_discharge_criteria_master_view'),
    path('master-confirm-section/<int:pk>/', confirm_master_view, name='confirm_master_view'),
    
    
    # """ MASTER DOCUMENT URLS """
    
    # FOCUS AREAS
    path('focus-area/add/<int:pk>/',create_focus_area, name='add_focusarea'),
    path('focus-area/<int:pk>/edit/',edit_focus_area, name='edit_focusarea'),
    path('focus-area/<int:pk>/delete/',delete_focus_area, name='delete_focusarea'),
    
    # GOALS
    path('goal/add/<int:focus_area_id>/',create_goal, name='add_goal'),
    path('goal/<int:pk>/edit/',edit_goal, name='edit_goal'),
    path('goal/<int:pk>/delete/',delete_goal, name='delete_goal'),

    # OBJECTIVES
    path('objective/add/<int:goal_id>/',create_objective, name='add_objective'),
    path('objective/<int:pk>/edit/',edit_objective, name='edit_objective'),
    path('objective/<int:pk>/delete/',delete_objective, name='delete_objective'),

    # INTERVENTIONS
    path('intervention/add/<int:objective_id>/',create_intervention, name='add_intervention'),
    path('intervention/<int:pk>/edit/',edit_intervention, name='edit_intervention'),
    path('intervention/<int:pk>/delete/',delete_intervention, name='delete_intervention'),
    
    # Inline POSTs
    path('goal/add/inline/<int:focus_area_id>/',create_goal_inline, name='add_goal_inline'),
    path('objective/add/inline/<int:goal_id>/',create_objective_inline, name='add_objective_inline'),
    path('intervention/add/inline/<int:goal_id>/',create_intervention_inline, name='add_intervention_inline'),
    
    # """ END MASTER DOCUMENT URLS """
    
    
    # Section 5
    path('customer-section_five/<int:pk>/', section_five_view, name='section_five_view'),
    path('customer-section_five-history/<int:pk>/', section_five_document_three_history, name='section_five_document_three_history'),
    
    # Section 6
    # path('customer-section_six/<int:pk>/', section_six_view, name='section_six_view'),
]
