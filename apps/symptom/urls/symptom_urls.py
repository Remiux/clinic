from apps.symptom.views.symptom_view import *
from django.urls import path


urlpatterns = [
  
    path('symptoms', symptoms_view, name='symptoms_view'),
    path('filter-symptoms', filter_symptoms_view, name='filter_symptoms_view'),
    path('symptoms-create/', create_symptom_view, name='create_symptom_view'),
    path('symptoms-update/<int:pk>/', update_symptom_view, name='update_symptom_view'),
   
    
]
