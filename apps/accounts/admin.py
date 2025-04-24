from django.contrib import admin

from apps.accounts.models import User
from apps.symptom.models import Customer, EncryptedFileUser

# Register your models here.

admin.site.register(User)
admin.site.register(EncryptedFileUser)