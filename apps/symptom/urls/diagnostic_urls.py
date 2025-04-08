from apps.symptom.views.diagnostic_view import *
from django.urls import path


urlpatterns = [
  
    path('diagnostics/', diagnostics_view, name='diagnostics_view'),
    path('filter-diagnostics', filter_diagnostics_view, name='filter_diagnostics_view'),
    path('diagnostics-create/', create_diagnostic_view, name='create_diagnostic_view'),
    path('diagnostics-detail/<int:pk>/', detail_diagnostic_view, name='detail_diagnostic_view'),
    path('diagnostics-update/<int:pk>/', update_diagnostic_view, name='update_diagnostic_view'),
   
    
]
