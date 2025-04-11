from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.symptom.filters import ClientFilter, InsuranceFilter
from apps.symptom.form import CustomerForm, CustomerSignForm
from apps.symptom.models import Agency, Customer, Diagnostic, Insurance, Symptom
from utils.paginator import _get_paginator 
from apps.symptom.models import Customer
from django.contrib.auth import get_user_model
from apps.symptom.models import EncryptedFile
from apps.symptom.form import FileUploadForm

# Create your views here.
@login_required(login_url='/login')
def section_one_view(request,pk):
    context = {
        'customer':get_object_or_404(Customer, pk=pk),
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section1/index.html',context)
