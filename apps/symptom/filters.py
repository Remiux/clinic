from apps.symptom.models import Customer, Diagnostic, Symptom,Insurance, EncryptedFile, TherapistsGroups
import django_filters
from django.db.models.functions import Substr, Length

        
class SymptomFilter(django_filters.FilterSet):
    code =  django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Symptom
        fields = [ 'code']
        

            
class InsuranceFilter(django_filters.FilterSet):
    abbreviated =  django_filters.CharFilter(lookup_expr='icontains')
    name =  django_filters.CharFilter(lookup_expr='icontains')
    available =  django_filters.BooleanFilter()
    auth_required =  django_filters.BooleanFilter()
    
    class Meta:
        model = Insurance
        fields = [ 'abbreviated','name', 'available', 'auth_required']
        
class DiagnosticFilter(django_filters.FilterSet):
    code =  django_filters.CharFilter(lookup_expr='icontains')
   
    class Meta:
        model = Diagnostic
        fields = [ 'code']

class ClientFilter(django_filters.FilterSet):
    ssn = django_filters.CharFilter(lookup_expr='icontains')
    dob = django_filters.DateFilter(lookup_expr='exact')
    case_no =  django_filters.CharFilter(lookup_expr='icontains')
    first_name =  django_filters.CharFilter(lookup_expr='icontains')
    diagnostic = django_filters.ModelChoiceFilter(queryset=Diagnostic.objects.all())
    
    class Meta:
        model = Customer
        fields = [ 'ssn','dob','case_no','first_name','diagnostic']



class EncryptedFileFilter(django_filters.FilterSet):
    file = django_filters.CharFilter(method='filter_file_name', label='File Name')
    file_type = django_filters.ChoiceFilter(choices=EncryptedFile._meta.get_field('file_type').choices, lookup_expr='icontains')
    uploaded_by = django_filters.CharFilter(field_name='uploaded_by__username', lookup_expr='icontains')
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='date')  # Filtro por fecha de creación
    
    
    class Meta:
        model = EncryptedFile
        fields = ['file', 'file_type', 'uploaded_by', 'created_at']

    def filter_file_name(self, queryset, name, value):
        # Extraer solo el nombre del archivo (sin la ruta)
        return queryset.annotate(
            file_name=Substr('file', Length('file') - Length('file') + 1)
        ).filter(file_name__icontains=value)
        
        

class TherapistsGroupsFilter(django_filters.FilterSet):
    therapist_first_name = django_filters.CharFilter(field_name='therapist__first_name', lookup_expr='icontains')
    therapist_last_name = django_filters.CharFilter(field_name='therapist__last_name', lookup_expr='icontains')
    section =  django_filters.CharFilter(lookup_expr='exact')
    
    class Meta:
        model = TherapistsGroups
        fields = ['therapist_first_name','therapist_last_name','section']