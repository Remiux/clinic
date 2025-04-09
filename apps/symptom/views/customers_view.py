from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.symptom.filters import InsuranceFilter
from apps.symptom.form import InsuranceForm
from apps.symptom.models import Insurance, Symptom
from utils.paginator import _get_paginator 
from apps.symptom.models import Customer
from django.contrib.auth import get_user_model
from apps.symptom.models import EncryptedFile

# Create your views here.
@login_required(login_url='/login')
def customers_view(request):
    customers = Customer.objects.all()
    files = EncryptedFile.objects.filter(belongs_to=request.user)
    context = {'customers': customers, 'files': files}
    return render(request,'pages/customers/index.html',context)


@login_required(login_url='/login')
def detail_customer_view(request,pk):
    User = get_user_model()
    users = User.objects.all()
    files = EncryptedFile.objects.filter(belongs_to=request.user)
    customer = get_object_or_404(Customer, pk=pk)
    context = {'customer': customer, 'users': users, 'files': files}
    return render(request,'pages/customers/actions/detail/customerDetail.html',context)

@login_required(login_url='/login')
def sign_customer_view(request, pk):
    context={}
    return render(request, 'pages/customers/actions/detail/customerGenerateSign.html', context)