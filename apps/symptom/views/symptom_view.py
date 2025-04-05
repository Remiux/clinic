from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from apps.symptom.filters import SymptomFilter
from apps.symptom.form import SymptomForm
from apps.symptom.models import Symptom
from utils.paginator import _get_paginator 


# Create your views here.
@login_required(login_url='/login')
def symptoms_view(request):
    context=_show_symptoms_filter(request)
    return render(request,'pages/symptoms/index.html',context)


def create_symptom_view(request):
    form = SymptomForm(request.POST or None)
    context={}
    if request.method == "POST":
        if form.is_valid():
            form.save()
            context['message']='Successfull'
            form=SymptomForm()
        else:
            pass
    context['form']=form
    return render(request,'pages/symptoms/actions/form/symptomFormCreate.html',context)


@login_required(login_url='/login')
def filter_symptoms_view(request):
    context=_show_symptoms_filter(request)
    return render(request,'pages/symptoms/symptomTable.html',context)

@login_required(login_url='/login')
def detail_symptom_view(request,pk):
    symptom = get_object_or_404(Symptom,pk=pk)
    
    context={}
    if symptom:
        context['symptom']=symptom
    return render(request,'pages/symptoms/actions/symptomDetail.html',context)

def _show_symptoms_filter(request):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    symptoms = SymptomFilter(request.GET, queryset=Symptom.objects.all().order_by('code'))
    context = _get_paginator(request, symptoms.qs)
    context['parameters'] = parameters
    return context

@login_required(login_url='/login')
def update_symptom_view(request,pk):
    symptom = get_object_or_404(Symptom,pk=pk)
    form = SymptomForm(request.POST or None,instance=symptom)
    context={}
    if request.method == "POST":  
        if form.is_valid():
            form.save()
            context['message']='Successfull'
        else:
            pass
    context['form']=form
    context['symptom']=symptom
    return render(request,'pages/symptoms/actions/symptomUpdate.html',context)