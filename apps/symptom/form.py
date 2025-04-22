from django import forms
from apps.symptom.models import Diagnostic, Symptom,Insurance, Customer, EncryptedFile
from apps.accounts.models import User

class SymptomForm(forms.ModelForm):
    
    class Meta:
        model = Symptom
        fields = '__all__'


class InsuranceForm(forms.ModelForm):
    
    class Meta:
        model = Insurance
        fields = '__all__'
    
class DiagnosticForm(forms.ModelForm):
    
    class Meta:
        model = Diagnostic
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        exclude = ['sign','create_at','medicaid_gold_card','responsible_payee_last_name',
                   'responsible_payee_first_name','responsible_payee_address','responsible_payee_city',
                   'responsible_payee_state','responsible_payee_zip','responsible_payee_phone_number','responsible_payee_fax'
                   ,'no_dependences','family_year_income','discount_standard_rate','discount_standard_rate']
        
class CustomerSignForm(forms.ModelForm):
    
    class Meta:
        model = Customer
        fields = ['sign']
        


from apps.symptom.models import EncryptedFile

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = EncryptedFile
        fields = ['file', 'process_start_date']

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        
        if file:
            # Obtener la extensión del archivo subido
            file_extension = file.name.split('.')[-1].lower()

            # Definir el mapeo de extensiones permitidas
            file_type_mapping = {
                'docx': '.docx',
                'doc': '.doc',
                'pdf': '.pdf',
                'jpg': '.jpg',
                'jpeg': '.jpg',  # Tratar JPEG como JPG
                'png': '.png',
            }

            # Verificar si la extensión es válida
            if file_extension not in file_type_mapping:
                raise forms.ValidationError(
                    f"La extensión del archivo ({file_extension}) no es válida. Solo se permiten: {', '.join(file_type_mapping.keys())}."
                )

        return cleaned_data


