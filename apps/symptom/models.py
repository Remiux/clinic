from django.db import models
from solo.models import SingletonModel
from apps.accounts.models import User
from django.utils import timezone
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


# Create your models here.

class Agency(SingletonModel):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=70)
    zip = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=40)
    fax = models.CharField(max_length=40)

    class Meta:
        verbose_name = "Agency"
        verbose_name_plural = "Agencys"

    def __str__(self):
        return self.name





class Medication(models.Model):
    name = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField()
    customer = models.ForeignKey(
        'Customer', 
        on_delete=models.CASCADE, 
        related_name='medications'
    )

    class Meta:
        verbose_name = "Medication"
        verbose_name_plural = "Medications"

    def __str__(self):
        return f"{self.name} ({self.quantity}mg)"
    
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
    
class Diagnostic(models.Model):
    code = models.CharField(max_length=15, unique=True)
    description = models.TextField(max_length=500)
    # customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='diagnostics', null=True, blank=True)
    
    class Meta:
        verbose_name = "Diagnostic"
        verbose_name_plural = "Diagnostics"

    def __str__(self):
        return self.code


class Customer(models.Model):
    case_no = models.CharField(max_length=40, unique=True)
    create_at = models.DateField(auto_created=True,default=timezone.now)
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
    dob = models.DateField(default=timezone.now)
    gender = models.CharField(max_length=50, default='M', choices=[('M', 'MALE'), ('F', 'FEMALE')])
    ssn = models.CharField(max_length=50, unique=True)
    mma = models.CharField(max_length=50, null=True, blank=True)
    medicaid_no = models.CharField(max_length=50, unique=True)
    medicare_no = models.CharField(max_length=50, null=True, blank=True)
    school = models.CharField(max_length=50, null=True, blank=True)
    grade = models.CharField(max_length=50, null=True, blank=True)
    race = models.CharField(max_length=50,default='W' ,choices=[('W', 'White'), ('AAB', 'African American Black'), ('API', 'Asian or Other Pacific Islander'), ('AIAN', 'American Indian-Alaskan Native'), ('O', 'Other')])
    referred_by = models.CharField(max_length=50, blank=True, null=True)
    referred_movile = models.IntegerField(blank=True, null=True)
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
    medicaid_gold_card = models.CharField(max_length=50, unique=True, null=True, blank=True)
    responsible_payee_last_name = models.CharField(max_length=50, null=True, blank=True, default="N/A")
    responsible_payee_first_name = models.CharField(max_length=50, null=True, blank=True, default="N/A")
    responsible_payee_address = models.CharField(max_length=150, null=True, blank=True, default="N/A")
    responsible_payee_city = models.CharField(max_length=80, null=True, blank=True, default="N/A")
    responsible_payee_state = models.CharField(max_length=80, null=True, blank=True, default="N/A")
    responsible_payee_zip = models.CharField(max_length=80, null=True, blank=True, default="N/A")
    responsible_payee_phone_number = models.CharField(max_length=20, null=True, blank=True, default="N/A")
    responsible_payee_fax = models.CharField(max_length=20, null=True, blank=True, default="N/A")
    no_dependences = models.PositiveIntegerField(default=0)
    family_year_income = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    discount_standard_rate = models.DecimalField(max_digits=15, decimal_places=2, default=0.00,null=True, blank=True)
    sign = models.ImageField(upload_to='customer_sign',blank=True,null=True)
    insurance = models.ForeignKey(Insurance, on_delete=models.CASCADE)
    insurance_unit = models.PositiveIntegerField(default=0)
    insurance_init_date = models.DateField(null=True,blank=True)
    insurance_end_date = models.DateField(null=True,blank=True)
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)
    diagnostic_two = models.ForeignKey(Diagnostic, on_delete=models.CASCADE,null=True,blank=True, related_name='diagnostic_two_client')
    diagnostic_three = models.ForeignKey(Diagnostic, on_delete=models.CASCADE,null=True,blank=True, related_name='diagnostic_three_client')
    treatment_duration = models.PositiveIntegerField(
        default=6,
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )
    treatment_plan_developed_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when the treatment plan was developed."
    )

    # def clean(self):
    #     from django.core.exceptions import ValidationError
    #     # Validar que la fecha no coincida con ninguna fecha de atención de terapeutas
    #     if self.treatment_plan_developed_date:
    #         # Verificar en terapias individuales
    #         individual_therapy_dates = IndividualTherapySection.objects.filter(
    #             customer=self,
    #             create_at=self.treatment_plan_developed_date
    #         )
    #         if individual_therapy_dates.exists():
    #             raise ValidationError(
    #                 {"treatment_plan_developed_date": "The treatment plan developed date cannot coincide with any therapist's session date."}
    #             )

    #         # Verificar en sesiones grupales
    #         group_therapy_dates = CustomerPSRSections.objects.filter(
    #             customer=self,
    #             section__create_at=self.treatment_plan_developed_date
    #         )
    #         if group_therapy_dates.exists():
    #             raise ValidationError(
    #                 {"treatment_plan_developed_date": "The treatment plan developed date cannot coincide with any group session date."}
    #             )

    #     super().clean()

 
    
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
    file_type = models.CharField(max_length=10, choices=[('.docx', 'DOCX'), ('.doc', 'DOC'), ('.pdf', 'PDF'), ('.jpg', 'JPG'), ('.png', 'PNG')])
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    belongs_to = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='owned_files', default=1)
    encrypted_file = models.BinaryField()
    created_at = models.DateTimeField(default=timezone.now)
    process_start_date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Asignar automáticamente el file_type basado en la extensión del archivo
        if self.file and not self.file_type:
            extension = self.file.name.split('.')[-1].lower()
            file_type_mapping = {
                'docx': '.docx',
                'doc': '.doc',
                'pdf': '.pdf',
                'jpg': '.jpg',
                'jpeg': '.jpg',  # Tratar JPEG como JPG
                'png': '.png',
            }
            self.file_type = file_type_mapping.get(extension, None)
        super(EncryptedFile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.file.name} - {self.uploaded_by.username}"
    
    

class EncryptedFileUser(models.Model):
    file = models.FileField(upload_to='uploads/')
    file_type = models.CharField(max_length=10, choices=[('.docx', 'DOCX'), ('.doc', 'DOC'), ('.pdf', 'PDF'), ('.jpg', 'JPG'), ('.png', 'PNG')])
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files_user')
    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_files', default=1)
    encrypted_file = models.BinaryField()
    created_at = models.DateTimeField(default=timezone.now)
    process_start_date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Asignar automáticamente el file_type basado en la extensión del archivo
        if self.file and not self.file_type:
            extension = self.file.name.split('.')[-1].lower()
            file_type_mapping = {
                'docx': '.docx',
                'doc': '.doc',
                'pdf': '.pdf',
                'jpg': '.jpg',
                'jpeg': '.jpg',  # Tratar JPEG como JPG
                'png': '.png',
            }
            self.file_type = file_type_mapping.get(extension, None)
        super(EncryptedFileUser, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.file.name} - {self.uploaded_by.username}"

    
class Eligibility(models.Model):
    encrypted_file = models.OneToOneField(
        EncryptedFile, 
        on_delete=models.CASCADE, 
        related_name='eligibility'
    )
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Eligibility"
        verbose_name_plural = "Eligibilities"

    def __str__(self):
        return f"Eligibility for {self.encrypted_file.file.name}"
    
class SuicideRisk(models.Model):
    encrypted_file = models.OneToOneField(
        EncryptedFile, 
        on_delete=models.CASCADE, 
        related_name='suicide_risk'
    )
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "SuicideRisk"
        verbose_name_plural = "SuicideRisks"

    def __str__(self):
        return f"Suicide Risk for {self.encrypted_file.file.name}"
    
    
class BehavioralHealth(models.Model):
    encrypted_file = models.OneToOneField(
        EncryptedFile, 
        on_delete=models.CASCADE, 
        related_name='behavioral_health'
    )
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "BehavioralHealth"
        verbose_name_plural = "BehavioralHealths"

    def __str__(self):
        return f"Behavioral Health for {self.encrypted_file.file.name}"
    

class BioPsychoSocial(models.Model):
    encrypted_file = models.OneToOneField(
        EncryptedFile, 
        on_delete=models.CASCADE, 
        related_name='bio_psycho_social'
    )
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "BioPsychoSocialAssessment"
        verbose_name_plural = "BioPsychoSocialAssessments"

    def __str__(self):
        return f"Bio Psycho Social Assessment for {self.encrypted_file.file.name}"
    

class BriefBehavioralHealth(models.Model):
    encrypted_file = models.OneToOneField(
        EncryptedFile, 
        on_delete=models.CASCADE, 
        related_name='brief_behavioral_health'
    )
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "BriefBehavioralHealth"
        verbose_name_plural = "BriefBehavioralHealths"

    def __str__(self):
        return f"Brief Behavioral Health for {self.encrypted_file.file.name}"
    

class DischargeSummary(models.Model):
    encrypted_file = models.OneToOneField(
        EncryptedFile, 
        on_delete=models.CASCADE, 
        related_name='discharge_summary'
    )
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "DischargeSummary"
        verbose_name_plural = "DischargeSummaries"

    def __str__(self):
        return f"Discharge Summary for {self.encrypted_file.file.name}"

class PsychiatricEvaluation(models.Model):
    PROCEDENCE_CHOICES = [
        ('Fax', 'Fax'),
        ('Email', 'Email'),
        ('ClientDirectly', 'Client Directly'),
    ]
    
    encrypted_file = models.OneToOneField(
        EncryptedFile, 
        on_delete=models.CASCADE, 
        related_name='psychiatric_evaluation'
    )
    psychiatrist = models.CharField(max_length=70, default='N/A')
    procedence = models.CharField(max_length=20, choices=PROCEDENCE_CHOICES, default='ClientDirectly')
    observation = models.TextField(max_length=500, null=True, blank=True)
    

    class Meta:
        verbose_name = "PsiquiatricEvaluation"
        verbose_name_plural = "PsiquiatricEvaluations"

    def __str__(self):
        return f"PsiquiatricEvaluation for {self.encrypted_file.file.name}"
    
class YearlyPhysical(models.Model):
    encrypted_file = models.OneToOneField(
        EncryptedFile, 
        on_delete=models.CASCADE, 
        related_name='yearly_physical'
    )
    description = models.TextField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "YearlyPhysical"
        verbose_name_plural = "YearlyPhysicals"

    def __str__(self):
        return f"Yearly Physical for {self.encrypted_file.file.name}"

""" Nuevos Modelos """
class FocusArea(models.Model):
    TIPO_CHOICES = [
        ('PSR', 'PSR'),
        ('Individual', 'Individual Therapy'),
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='focus_areas')
    title = models.CharField(max_length=100)
    description = models.TextField(null=False, blank=False)
    focus_area_type = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return f"Focus Area {self.id}: {self.title}"

class Goal(models.Model):
    focus_area = models.ForeignKey(FocusArea, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"GOAL {self.id}: {self.title}"

class Objective(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    description = models.TextField('Just a description')
    open_date = models.DateField(default=timezone.now)
    close_date = models.DateField(default=timezone.now)
    static_text = models.TextField(default="Static text.")

    def __str__(self):
        return f"Objective {self.number} - GOAL {self.goal.id}"

class Intervention(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    description = models.TextField('Just a description')

    def __str__(self):
        return f"Object Intervention {self.goal.id} - {self.description}"


""" Fin nuevos modelos """


class FARS(models.Model):
    STATUS_CHOICES = [
        ('Initial', 'Initial'),
        ('Checked', 'Checked'),
        ('Finished', 'Finished'),
    ]
    
    encrypted_file = models.OneToOneField(
        EncryptedFile, 
        on_delete=models.CASCADE, 
        related_name='fars_document'
    )
    description = models.TextField(max_length=500, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Initial')

    class Meta:
        verbose_name = "FarsDocument"
        verbose_name_plural = "FarsDocuments"

    def __str__(self):
        return f"FarsDocument for {self.encrypted_file.file.name}"

    
class HistoricalSection1(models.Model):
    create_datetime_at = models.DateTimeField(auto_created=True,default=timezone.now)
    create_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_section1')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='historical_section1')
    date = models.DateField(default=timezone.now)
    
    class Meta:
        verbose_name = "HistoricalSection1"
        verbose_name_plural = "HistoricalSection1s"

    def __str__(self):
        return f"{self.pk}"

    
class TherapistsGroups(models.Model):
    type = models.BooleanField(default=False)  # True for PSR, False for Individual Therapy
    therapist = models.ForeignKey(User, on_delete=models.PROTECT, related_name='therapist_group', null=True)
    
    
    class Meta:
        verbose_name = "TherapistGroup"
        verbose_name_plural = "TherapistsGroups"

    def __str__(self):
        return f"{self.pk}-{self.type}-section"

    
class GroupCustomer(models.Model):
    group = models.ForeignKey(TherapistsGroups, on_delete=models.CASCADE, related_name='group_customer')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_group')
    is_active = models.BooleanField(default=True)
    max_sections = models.PositiveIntegerField( default=16 , validators=[MinValueValidator(1), MaxValueValidator(16)])
    
    class Meta:
        verbose_name = "GroupCustomer"
        verbose_name_plural = "GroupCustomers"

    def __str__(self):
        return f"{self.customer.full_name}"

class IndividualTherapy(models.Model):
    therapist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='individual_therapists')
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE, related_name='individual_customer')
    type = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "IndividualTherapy"
        verbose_name_plural = "IndividualTherapies"

    def __str__(self):
        return f"{self.customer.full_name} managed by {self.therapist.first_name}"
    
class IndividualTherapySection(models.Model):
    individual_therapy_pk =  models.CharField(max_length=20)
    therapist_pk = models.CharField(max_length=20)
    therapist_full_name = models.CharField(max_length=80)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_individual_therapy')
    create_at = models.DateField(auto_created=True,default=timezone.now)
    init_hour = models.TimeField(null=True, blank=True)
    end_hour = models.TimeField(null=True, blank=True)
    is_active= models.BooleanField(default=True)
    points = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])
    after_points = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])
    before_points = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])
    
    class Meta:
        verbose_name = "IndividualTherapySection"
        verbose_name_plural = "IndividualTherapiesSections"

    def __str__(self):
        return f"{self.pk}"


class GroupsPSRSections(models.Model):
    therapist_pk = models.CharField(max_length=20)
    therapist_full_name = models.CharField(max_length=80)
    group_pk = models.CharField(max_length=20)
    create_at = models.DateField(auto_created=True,default=timezone.now)
    init_hour = models.TimeField(null=True, blank=True)
    end_hour = models.TimeField(null=True, blank=True)
    is_active= models.BooleanField(default=True)

    class Meta:
        verbose_name = "GroupsPSRSections"
        verbose_name_plural = "GroupsPSRSectionss"

    def __str__(self):
        return f"{self.pk}"

    
class CustomerPSRSections(models.Model):
    section = models.ForeignKey(GroupsPSRSections, on_delete=models.CASCADE, related_name='customer_psr_section')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_psr_group')
    assist = models.BooleanField(default=False)
    points = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])
    after_points = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])
    before_points = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100000)])

    class Meta:
        verbose_name = "CustomerPSRSection"
        verbose_name_plural = "CustomerPSRSections"

    def __str__(self):
        return f"{self.pk}"
    
    @property
    def is_customer_group(self):
        group = TherapistsGroups.objects.filter(pk= int(self.section.group_pk)).first()
        if group:
            customer = group.group_customer.filter(customer = self.customer)
            if customer:
                return False
        return True