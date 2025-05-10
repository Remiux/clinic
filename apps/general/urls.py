from apps.general.views import index, test,login_view, load_section
from django.urls import path, include, re_path
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', index, name='index'),
    path('test', test, name='test'),
    path('login', login_view, name='login'),
    path('logout',LogoutView.as_view(),name='logout'),
    path('', include('apps.accounts.urls.users_urls')),
    path('', include('apps.accounts.urls.master_generate_urls')),
    path('', include('apps.symptom.urls.symptom_urls')),
    path('', include('apps.symptom.urls.insurance_urls')),
    path('load-section/<str:section_name>/', load_section, name='load_section'),
    path('', include('apps.symptom.urls.customer_urls')),
    path('', include('apps.symptom.urls.cryptography_urls')),
    path('', include('apps.symptom.urls.diagnostic_urls')),
    path('', include('apps.symptom.urls.sections_urls')),
    path('', include('apps.symptom.urls.therapists_groups_urls')),
    path('', include('apps.symptom.urls.individual_therapy_urls')),
    
    
]
