from django.contrib import admin
from apps.symptom.models import *

# Register your models here.

admin.site.register(Symptom)
admin.site.register(Client)
admin.site.register(EncryptedFile)
admin.site.register(Insurance)
admin.site.register(Diagnostic)