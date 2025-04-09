from django.db import models
from apps.accounts.models import User
from django.utils import timezone
import uuid


# Create your models here.

class Diagnostic(models.Model):
    code = models.CharField(max_length=15, unique=True)
    description = models.TextField(max_length=500)
    

    class Meta:
        verbose_name = "Diagnostic"
        verbose_name_plural = "Diagnostics"

    def __str__(self):
        return self.code

    
    
class Symptom(models.Model):
    code = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=1000)
    

    class Meta:
        verbose_name = "Symptom"
        verbose_name_plural = "Symptoms"

    def __str__(self):
        return self.code
    
class Insurance(models.Model):
    abbreviated = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255, unique=True)
    available = models.BooleanField(default=True)
    auth_required = models.BooleanField(default=True)
    

    class Meta:
        verbose_name = "Insurance"
        verbose_name_plural = "Insurances"

    def __str__(self):
        return self.name
    

class EncryptedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=10, choices=[('.docx', 'DOC'), ('.pdf', 'PDF'), ('.jpg', 'JPG'), ('.png', 'PNG')])
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_files')
    encrypted_file = models.BinaryField()
    created_at = models.DateTimeField(default=timezone.now)
    process_start_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.file.name} - {self.uploaded_by.username}"

class Client(models.Model):
    case_no = models.CharField(max_length=40, unique=True,default='FS0001')
    first_name = models.CharField(max_length=255,default='John')
    last_name = models.CharField(max_length=255,default='Doe')
    email = models.EmailField(unique=True,default='example@gmail.com')
    address = models.TextField(max_length=500,default='123 Main St, Springfield')
    contact_no = models.CharField(max_length=20,default='1234567890')
    home_phone = models.CharField(max_length=20, null=True, blank=True)
    movile = models.CharField(max_length=20,default='1234567890')
    city = models.CharField(max_length=50,default=' Springfield')
    state = models.CharField(max_length=50,default='IL')
    zip = models.CharField(max_length=50,default='62701')
    dob = models.DateField(default=timezone.now)
    gerder = models.CharField(max_length=50, default='M', choices=[('M', 'MALE'), ('F', 'FAMALE')])
    ssn = models.CharField(max_length=50, unique=True,default='1234567890')
    mma = models.CharField(max_length=50, null=True, blank=True)
    medicaid_no = models.CharField(max_length=50, unique=True,default='1234567890')
    medicare_no = models.CharField(max_length=50, null=True, blank=True)
    school = models.CharField(max_length=50, null=True, blank=True)
    grade = models.CharField(max_length=50, null=True, blank=True)
    race = models.CharField(max_length=50,default='W' ,choices=[('W', 'White'), ('AAB', 'African American Black'), ('API', 'Asian or Other Pacific Islander'), ('AIAN', 'American Indian-Alaskan Native'), ('O', 'Other')])
    ethnicity = models.CharField(max_length=50,default='H',choices=[('H', 'Hispanic-latino'), ('NH', 'Non-Hispanic'), ('O', 'Other')])
    legal_guardian_full_name = models.CharField(max_length=80, null=True, blank=True)
    legal_guardian_relationship = models.CharField(max_length=80, null=True, blank=True)
    legal_guardian_phone_number = models.CharField(max_length=80, null=True, blank=True)
    legal_guardian_address = models.CharField(max_length=150, null=True, blank=True)
    legal_guardian_city = models.CharField(max_length=80, null=True, blank=True)
    legal_guardian_state = models.CharField(max_length=80, null=True, blank=True)
    legal_guardian_zip = models.CharField(max_length=80, null=True, blank=True)
    emergency_contact_person = models.CharField(max_length=80,default='John Doe')
    emergency_contact_relationship = models.CharField(max_length=80,default='wife')
    emergency_contact_phone_number = models.CharField(max_length=20,default='1234567890')
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE, related_name='insurances_client')
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE, related_name='diagnostic_client')
    diagnostic_two = models.ForeignKey(Diagnostic, on_delete=models.CASCADE,null=True,blank=True, related_name='diagnostic_two_client')
    diagnostic_three = models.ForeignKey(Diagnostic, on_delete=models.CASCADE,null=True,blank=True, related_name='diagnostic_three_client')
    
    
    
    def save(self, *args, **kwargs):
        # if not self.code:
        #     self.code = uuid.uuid4().hex[:12].upper()  # Genera un código alfanumérico de 12 caracteres
        super(Client, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name }"
    
    @property
    def in_active(self):
        return True