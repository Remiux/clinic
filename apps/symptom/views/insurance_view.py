from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.symptom.filters import InsuranceFilter
from apps.symptom.form import InsuranceForm
from apps.symptom.models import Insurance, Symptom
from utils.paginator import _get_paginator 


# Create your views here.
@login_required(login_url='/login')
def insurances_view(request):
    context=_show_insurance_filter(request)
    return render(request,'pages/insurance/index.html',context)


def create_insurance_view(request):
    form = InsuranceForm(request.POST or None)
    context={}
    if request.method == "POST":
        if form.is_valid():
            form.save()
            context['message']='Successfull'
            form=InsuranceForm()
        else:
            pass
    context['form']=form
    return render(request,'pages/insurance/actions/form/insuranceFormCreate.html',context)


@login_required(login_url='/login')
def filter_insurances_view(request):
    context=_show_insurance_filter(request)
    return render(request,'pages/insurance/insuranceTable.html',context)

@login_required(login_url='/login')
def detail_insurance_view(request,pk):
    insurance = get_object_or_404(Insurance,pk=pk)
    
    context={}
    if insurance:
        context['insurance']=insurance
    return render(request,'pages/insurance/actions/insuranceDetail.html',context)

def _show_insurance_filter(request):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    insurance = InsuranceFilter(request.GET, queryset=Insurance.objects.all().order_by('name'))
    context = _get_paginator(request, insurance.qs)
    context['parameters'] = parameters
    return context

@login_required(login_url='/login')
def update_insurance_view(request,pk):
    insurance = get_object_or_404(Insurance,pk=pk)
    form = InsuranceForm(request.POST or None,instance=insurance)
    context={}
    if request.method == "POST":  
        if form.is_valid():
            form.save()
            context['message']='Successfull'
        else:
            pass
    context['form']=form
    context['insurance']=insurance
    return render(request,'pages/insurance/actions/insuranceUpdate.html',context)