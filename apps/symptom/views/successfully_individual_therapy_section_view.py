from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.symptom.filters import IndividualTherapySectionFilter, InsuranceFilter
from apps.symptom.form import InsuranceForm
from apps.symptom.models import IndividualTherapySection, Insurance, Symptom
from utils.paginator import _get_paginator 


# Create your views here.
@login_required(login_url='/login')
def successfully_individual_therapy_section_view(request):
    context=_show_successfully_individual_therapy_section_filter(request)
    return render(request,'pages/sections_successfully/individual_therapy_section/index.html',context)



@login_required(login_url='/login')
def filter_successfully_individual_therapy_section_view(request):
    context=_show_successfully_individual_therapy_section_filter(request)
    return render(request,'pages/sections_successfully/individual_therapy_section/individualTherapySectionTable.html',context)


def _show_successfully_individual_therapy_section_filter(request):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    insurance = IndividualTherapySectionFilter(request.GET, queryset=IndividualTherapySection.objects.filter(is_active=False).order_by('pk'))
    context = _get_paginator(request, insurance.qs)
    context['parameters'] = parameters
    return context
