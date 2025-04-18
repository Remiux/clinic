from django.contrib import admin
from apps.symptom.models import *

# Register your models here.

admin.site.register(Symptom)
# admin.site.register(Customer)
admin.site.register(EncryptedFile)
admin.site.register(Insurance)
admin.site.register(Diagnostic)
admin.site.register(Agency)
admin.site.register(HistoricalSection1)
admin.site.register(Medication)
admin.site.register(Eligibility)