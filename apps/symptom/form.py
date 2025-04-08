from django import forms
from apps.symptom.models import Diagnostic, Symptom,Insurance
from apps.accounts.models import User

class SymptomForm(forms.ModelForm):
    
    class Meta:
        model = Symptom
        fields = '__all__'


class InsuranceForm(forms.ModelForm):
    
    class Meta:
        model = Insurance
        fields = '__all__'


class FileUploadForm(forms.Form):
    file = forms.FileField()
    file_type = forms.ChoiceField(choices=[('.doc', 'DOC'), ('.pdf', 'PDF'), ('.jpg', 'JPG'), ('.png', 'PNG')])
    belongs_to = forms.ModelChoiceField(queryset=User.objects.all())
    process_start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de inicio del proceso"
    )
    
class DiagnosticForm(forms.ModelForm):
    
    class Meta:
        model = Diagnostic
        fields = '__all__'
