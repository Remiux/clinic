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
    

class Customer(models.Model):
    case_no = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.TextField(max_length=500)
    contact_no = models.CharField(max_length=20, null=True, blank=True)
    home_phone = models.CharField(max_length=20, null=True, blank=True)
    movile = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=50)
    dob = models.DateField()
    gerder = models.CharField(max_length=50, default='M', choices=[('M', 'MALE'), ('F', 'FAMALE')])
    ssn = models.CharField(max_length=50, unique=True)
    mma = models.CharField(max_length=50, null=True, blank=True)
    medicaid_no = models.CharField(max_length=50, unique=True)
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
    emergency_contact_person = models.CharField(max_length=80)
    emergency_contact_relationship = models.CharField(max_length=80)
    emergency_contact_phone_number = models.CharField(max_length=20)
    sign = models.ImageField(upload_to='customer_sign',blank=True,null=True)
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE)
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)
    diagnostic_two = models.ForeignKey(Diagnostic, on_delete=models.CASCADE,null=True,blank=True, related_name='diagnostic_two_client')
    diagnostic_three = models.ForeignKey(Diagnostic, on_delete=models.CASCADE,null=True,blank=True, related_name='diagnostic_three_client')
    
    
    
    def save(self, *args, **kwargs):
        # if not self.code:
        #     self.code = uuid.uuid4().hex[:12].upper()  # Genera un código alfanumérico de 12 caracteres
        super(Customer, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name }"
    
    @property
    def in_active(self):
        return True
    
    @property
    def years_old(self):
        from datetime import date
        today = date.today()
        age = today.year - self.dob.year
        if (today.month, today.day) < (self.dob.month, self.dob.day):
            age -= 1
        return age


class EncryptedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=10, choices=[('.docx', 'DOC'), ('.pdf', 'PDF'), ('.jpg', 'JPG'), ('.png', 'PNG')])
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    belongs_to = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='owned_files', default=1)
    encrypted_file = models.BinaryField()
    created_at = models.DateTimeField(default=timezone.now)
    process_start_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.file.name} - {self.uploaded_by.username}"