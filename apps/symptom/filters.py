from apps.symptom.models import Symptom
import django_filters

        
class SymptomFilter(django_filters.FilterSet):
    name =  django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = Symptom
        fields = [ 'name']
        