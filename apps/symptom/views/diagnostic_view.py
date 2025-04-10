from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from apps.symptom.filters import DiagnosticFilter
from apps.symptom.form import DiagnosticForm
from apps.symptom.models import Diagnostic
from utils.paginator import _get_paginator 


# Create your views here.
@login_required(login_url='/login')
def diagnostics_view(request):
    context=_show_diagnostics_filter(request)
    return render(request,'pages/diagnostic/index.html',context)


def create_diagnostic_view(request):
    form = DiagnosticForm(request.POST or None)
    context={}
    if request.method == "POST":
        if form.is_valid():
            form.save()
            context['message']='Successfull'
            form=DiagnosticForm()
        else:
            pass
    context['form']=form
    return render(request,'pages/diagnostic/actions/form/diagnosticFormCreate.html',context)


@login_required(login_url='/login')
def filter_diagnostics_view(request):
    context=_show_diagnostics_filter(request)
    return render(request,'pages/diagnostic/diagnosticTable.html',context)

@login_required(login_url='/login')
def detail_diagnostic_view(request,pk):
    diagnostic = get_object_or_404(Diagnostic,pk=pk)
    
    context={}
    if diagnostic:
        context['diagnostic']=diagnostic
    return render(request,'pages/diagnostic/actions/diagnosticDetail.html',context)

def _show_diagnostics_filter(request):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    diagnostics = DiagnosticFilter(request.GET, queryset=Diagnostic.objects.all().order_by('code'))
    context = _get_paginator(request, diagnostics.qs)
    context['parameters'] = parameters
    return context

@login_required(login_url='/login')
def update_diagnostic_view(request,pk):
    diagnostic = get_object_or_404(Diagnostic,pk=pk)
    form = DiagnosticForm(request.POST or None,instance=diagnostic)
    context={}
    if request.method == "POST":  
        if form.is_valid():
            form.save()
            context['message']='Successfull'
        else:
            pass
    context['form']=form
    context['diagnostic']=diagnostic
    return render(request,'pages/diagnostic/actions/diagnosticUpdate.html',context)