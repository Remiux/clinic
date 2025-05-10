from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.symptom.models import Agency, Customer, HistoricalSection1, Eligibility, PsychiatricEvaluation, YearlyPhysical, FARS
from apps.symptom.models import Customer
from django.db.models import Case, When, Value, IntegerField


@login_required(login_url='/login')
def section_five_view(request,pk):
    context = {
        'customer':get_object_or_404(Customer, pk=pk),
        'elegibility': Eligibility.objects.filter(encrypted_file__belongs_to=pk).order_by('-created_at').first(),
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section5/index.html', context)


@login_required(login_url='/login')
def section_five_document_three_history(request,pk):
    customer=get_object_or_404(Customer, pk=pk)     
    
    # Orden personalizado para el campo 'status'
    fars = FARS.objects.filter(encrypted_file__belongs_to=pk).annotate(
        custom_order=Case(
            When(status='Finished', then=Value(1)),
            When(status='Checked', then=Value(2)),
            When(status='Initial', then=Value(3)),
            output_field=IntegerField(),
        )
    ).order_by('custom_order', '-encrypted_file__created_at')
    
    context = {
        'fars': fars, #FARS.objects.filter(encrypted_file__belongs_to=pk).order_by('-encrypted_file__created_at'),
        'customer':customer,
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section5/history.html',context)