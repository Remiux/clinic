from django import forms
from apps.symptom.models import Symptom

class SymptomForm(forms.ModelForm):
    
    class Meta:
        model = Symptom
        fields = '__all__'




