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
admin.site.register(PsychiatricEvaluation)
admin.site.register(YearlyPhysical)
admin.site.register(SuicideRisk)
admin.site.register(BehavioralHealth)
admin.site.register(BioPsychoSocial)
admin.site.register(BriefBehavioralHealth)
admin.site.register(DischargeSummary)
admin.site.register(IndividualTherapy)
admin.site.register(IndividualTherapySection)
admin.site.register(FocusArea)
admin.site.register(Goal)
admin.site.register(Objective)
admin.site.register(Intervention)


class AdminGroupCustomer(admin.TabularInline):
    model = GroupCustomer
    extra = 0

@admin.register(TherapistsGroups)
class AdminTherapistsGroups(admin.ModelAdmin):
    list_display = ['pk', 'type']
    inlines = [AdminGroupCustomer,]
    list_per_page = 100
    

class AdminCustomerPSRSections(admin.TabularInline):
    model = CustomerPSRSections
    extra = 0

@admin.register(GroupsPSRSections)
class AdminGroupsPSRSections(admin.ModelAdmin):
    list_display = ['pk', 'therapist_full_name', 'therapist_pk', 'group_pk', 'is_active']
    inlines = [AdminCustomerPSRSections,]
    list_per_page = 100
    