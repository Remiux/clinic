from apps.symptom.models import Customer, Diagnostic, Symptom,Insurance
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
        