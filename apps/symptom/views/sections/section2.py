from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.symptom.models import Agency, Customer, HistoricalSection1
from apps.symptom.models import Customer
from django.http import HttpResponse
from django.template.loader import render_to_string


@login_required(login_url='/login')
def section_two_view(request,pk):
    context = {
        'customer':get_object_or_404(Customer, pk=pk),
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section2/index.html', context)