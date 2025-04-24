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
admin.site.register(Therapist)
admin.site.register(PsychiatricEvaluation)



class AdminGroupCustomer(admin.TabularInline):
    model = GroupCustomer
    extra = 0

@admin.register(TherapistsGroups)
class AdminTherapistsGroups(admin.ModelAdmin):
    list_display = ['pk', 'type','section']
    inlines = [AdminGroupCustomer,]
    list_per_page = 100