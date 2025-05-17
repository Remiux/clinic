from apps.accounts.models import User,MasterGenerate
import django_filters

        
class UserFilter(django_filters.FilterSet):
    username =  django_filters.CharFilter(lookup_expr='icontains')
    phone_number =  django_filters.CharFilter(lookup_expr='icontains')
    is_active =  django_filters.BooleanFilter()

    class Meta:
        model = User
        fields = [ 'username','phone_number','is_active']
        
        
class MasterGenerateFilter(django_filters.FilterSet):
    customer_pk =  django_filters.CharFilter(lookup_expr='exact')
    is_active =  django_filters.BooleanFilter()

    class Meta:
        model = MasterGenerate
        fields = [ 'customer_pk','is_active']
        