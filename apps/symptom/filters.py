from apps.symptom.models import Customer, Diagnostic, Symptom,Insurance, EncryptedFile
import django_filters

        
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
    file = django_filters.CharFilter(field_name='file', lookup_expr='icontains')  # Filtro por nombre del archivo
    file_type = django_filters.ChoiceFilter(choices=EncryptedFile._meta.get_field('file_type').choices)  # Filtro por tipo de archivo
    uploaded_by = django_filters.CharFilter(field_name='uploaded_by__username', lookup_expr='icontains')  # Filtro por usuario que subió el archivo
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='date')  # Filtro por fecha de creación

    class Meta:
        model = EncryptedFile
        fields = ['file', 'file_type', 'uploaded_by', 'created_at']