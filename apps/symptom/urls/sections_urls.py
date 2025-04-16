from apps.symptom.views.insurance_view import *
from django.urls import path

from apps.symptom.views.sections.section1 import *
from apps.symptom.views.sections.section2 import *


urlpatterns = [
    # Section 1
    path('customer-section_one/<int:pk>/', section_one_view, name='section_one_view'),
    path('customer-section_one-export-pdf/<int:pk>/', section_one_document_one_export_pdf, name='section_one_document_one_export_pdf'),
    path('customer-section_one-history/<int:pk>/', section_one_document_one_history, name='section_one_document_one_history'),
    
    
    # Section 2
    path('customer-section_two/<int:pk>/', section_two_view, name='section_two_view'), 
      
    # Section 3
    # path('customer-section_three/<int:pk>/', section_three_view, name='section_three_view'),
    
    # Section 4
    # path('customer-section_four/<int:pk>/', section_four_view, name='section_four_view'),
    
    # Section 5
    # path('customer-section_five/<int:pk>/', section_five_view, name='section_five_view'),
    
    # Section 6
    # path('customer-section_six/<int:pk>/', section_six_view, name='section_six_view'),
]
