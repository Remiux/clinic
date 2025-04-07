from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.symptom.filters import InsuranceFilter
from apps.symptom.form import InsuranceForm
from apps.symptom.models import Insurance, Symptom
from utils.paginator import _get_paginator 


# Create your views here.
@login_required(login_url='/login')
def customers_view(request):
    context={}
    return render(request,'pages/customers/index.html',context)

# Create your views here.
@login_required(login_url='/login')
def detail_customer_view(request,pk):
    context={}
    return render(request,'pages/customers/actions/detail/customerDetail.html',context)