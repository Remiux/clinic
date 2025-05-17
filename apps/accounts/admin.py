from django.contrib import admin

from apps.accounts.models import User,MasterGenerate
from apps.symptom.models import EncryptedFileUser

# Register your models here.

admin.site.register(User)
admin.site.register(EncryptedFileUser)
admin.site.register(MasterGenerate)
