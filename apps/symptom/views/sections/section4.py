from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.symptom.models import *
from django.http import HttpResponse
from django.template.loader import render_to_string
from apps.symptom.form import FileUploadForm
from utils.file_extension import get_file_extension
from apps.symptom.utils import encrypt_file, decrypt_file


@login_required(login_url='/login')
def section_four_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    # Verificar si el cliente está asociado a alguna IndividualTherapy
    is_in_individual_therapy = IndividualTherapy.objects.filter(customer=customer).exists()
    
    # Verificar si el cliente está asociado a algún GroupCustomer
    is_in_group_customer = GroupCustomer.objects.filter(customer=customer).exists()
    
    context = {
        'customer': customer,
        'agency': Agency.objects.first(),
        'is_in_individual_therapy': is_in_individual_therapy,
        'is_in_group_customer': is_in_group_customer,
    }
    return render(request, 'pages/customers/actions/sections/section4/index.html', context)

@login_required(login_url='/login')
def section_four_document_suicida_risk_history(request,pk):
    customer=get_object_or_404(Customer, pk=pk)     
    context = {
        'suicide_risks': SuicideRisk.objects.filter(encrypted_file__belongs_to=pk).order_by('-encrypted_file__created_at'),
        'customer':customer,
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section4/components/history_suicide_risk.html',context)


@login_required(login_url='/login')
def section_four_document_behavioral_health_history(request,pk):
    customer=get_object_or_404(Customer, pk=pk)     
    context = {
        'behavioral_health_evaluations': BehavioralHealth.objects.filter(encrypted_file__belongs_to=pk).order_by('-encrypted_file__created_at'),
        'customer':customer,
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section4/components/history_behavioral_health.html',context)


@login_required(login_url='/login')
def section_four_document_bio_psycho_social_history(request,pk):
    customer=get_object_or_404(Customer, pk=pk)     
    context = {
        'bio_psycho_social_assessments': BioPsychoSocial.objects.filter(encrypted_file__belongs_to=pk).order_by('-encrypted_file__created_at'),
        'customer':customer,
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section4/components/history_bio_psycho_social.html',context)


@login_required(login_url='/login')
def section_four_document_brief_behavioral_health_history(request,pk):
    customer=get_object_or_404(Customer, pk=pk)     
    context = {
        'brief_behavioral_health_assessments': BriefBehavioralHealth.objects.filter(encrypted_file__belongs_to=pk).order_by('-encrypted_file__created_at'),
        'customer':customer,
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section4/components/history_brief_behavioral_health.html',context)


@login_required(login_url='/login')
def section_four_document_discharge_summary_history(request,pk):
    customer=get_object_or_404(Customer, pk=pk)     
    context = {
        'discharge_sumaries': DischargeSummary.objects.filter(encrypted_file__belongs_to=pk).order_by('-encrypted_file__created_at'),
        'customer':customer,
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section4/components/history_discharge_sumary.html',context)