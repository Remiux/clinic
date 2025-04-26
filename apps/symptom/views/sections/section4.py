from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.symptom.models import Agency, Customer, HistoricalSection1, Eligibility, PsychiatricEvaluation, YearlyPhysical
from apps.symptom.models import Customer
from django.http import HttpResponse
from django.template.loader import render_to_string
from apps.symptom.form import FileUploadForm
from utils.file_extension import get_file_extension
from apps.symptom.utils import encrypt_file, decrypt_file


@login_required(login_url='/login')
def section_four_view(request,pk):
    context = {
        'customer':get_object_or_404(Customer, pk=pk),
        #'elegibility': Eligibility.objects.filter(encrypted_file__belongs_to=pk).order_by('-created_at').first(),
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section4/index.html', context)