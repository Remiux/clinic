from apps.symptom.views.therapists_groups_view import *
from apps.symptom.views.customers_view import *
from django.urls import path


urlpatterns = [
    path('groups/', therapists_groups_view, name='therapists_groups_view'),
    path('groups-filter/', filter_therapists_groups_view, name='filter_therapists_groups_view'),
    path('group-detail/<int:pk>/', detail_therapists_groups_view, name='detail_therapists_groups_view'),
   
]
