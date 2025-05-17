from django import forms
from apps.accounts.models import MasterGenerate, User


class CreateGenerateMasterForm(forms.ModelForm):
    
    
    class Meta:
        model = MasterGenerate
        exclude = ['user','create_at','is_active','customer_pk','customer_full_name']


