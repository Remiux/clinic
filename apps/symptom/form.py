from django import forms
from apps.symptom.models import Symptom,Insurance

class SymptomForm(forms.ModelForm):
    
    class Meta:
        model = Symptom
        fields = '__all__'


class InsuranceForm(forms.ModelForm):
    
    class Meta:
        model = Insurance
        fields = '__all__'


