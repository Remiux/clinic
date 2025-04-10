from django.contrib import admin
from apps.symptom.models import Customer  

# Registra el modelo Client en el admin
admin.site.register(Customer)