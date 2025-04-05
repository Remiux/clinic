from django.db import models

# Create your models here.

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