from django.db import models

# Create your models here.

class Symptom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    

    class Meta:
        verbose_name = "Symptom"
        verbose_name_plural = "Symptoms"

    def __str__(self):
        return self.name