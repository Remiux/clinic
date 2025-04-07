from apps.symptom.views.insurance_view import *
from django.urls import path


urlpatterns = [
  
    path('insurances', insurances_view, name='insurances_view'),
    path('filter-insurances', filter_insurances_view, name='filter_insurances_view'),
    path('insurances-create/', create_insurance_view, name='create_insurance_view'),
    path('insurances-detail/<int:pk>/', detail_insurance_view, name='detail_insurance_view'),
    path('insurances-update/<int:pk>/', update_insurance_view, name='update_insurance_view'),
   
    
]
