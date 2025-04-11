from django import forms
from apps.symptom.models import Diagnostic, Symptom,Insurance
from apps.accounts.models import User
from apps.symptom.models import Customer

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
    file_type = forms.ChoiceField(choices=[('.docx', 'DOCX'), ('.doc', 'DOC'), ('.pdf', 'PDF'), ('.jpg', 'JPG'), ('.png', 'PNG')])  # Cambiar PNG y JPG por Image
    belongs_to = forms.ModelChoiceField(queryset=Customer.objects.all(), widget=forms.HiddenInput())
    process_start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Fecha de inicio del proceso"
    )

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        file_type = cleaned_data.get('file_type')

        if file and file_type:
            # Obtener la extensión del archivo subido
            file_extension = f".{file.name.split('.')[-1].lower()}"

            # Definir extensiones permitidas para cada tipo
            allowed_extensions = {
                '.doc': ['.doc', '.docx'],  # Permitir .doc y .docx para .doc
                '.pdf': ['.pdf'],
                '.jpg': ['.jpg', '.jpeg', '.gif', '.bmp', '.tiff'],
                '.png': ['.png'],
            }

            # Verificar si la extensión del archivo está permitida
            if file_type not in allowed_extensions:
                raise forms.ValidationError(f"El tipo de archivo seleccionado ({file_type}) no es válido.")

            if file_extension not in allowed_extensions[file_type]:
                raise forms.ValidationError(
                    f"La extensión del archivo ({file_extension}) no coincide con el tipo seleccionado ({file_type})."
                )
        return cleaned_data
    
class DiagnosticForm(forms.ModelForm):
    
    class Meta:
        model = Diagnostic
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        exclude = ['sign']
        
class CustomerSignForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ['sign']