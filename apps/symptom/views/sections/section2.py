from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.symptom.models import Agency, Customer, HistoricalSection1, Eligibility
from apps.symptom.models import Customer
from django.http import HttpResponse
from django.template.loader import render_to_string
from apps.symptom.form import FileUploadForm
from utils.file_extension import get_file_extension
from apps.symptom.utils import encrypt_file, decrypt_file


@login_required(login_url='/login')
def section_two_view(request,pk):
    context = {
        'customer':get_object_or_404(Customer, pk=pk),
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section2/index.html', context)


@login_required(login_url='/login')
def section_two_document_two_history(request,pk):
    customer=get_object_or_404(Customer, pk=pk)     
    context = {
        'eligibilities':Eligibility.objects.filter(encrypted_file__belongs_to=pk).order_by('-created_at'),
        'customer':customer,
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section2/history.html',context)
