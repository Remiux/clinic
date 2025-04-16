from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.symptom.models import Agency, Customer, HistoricalSection1
from apps.symptom.models import Customer
from django.http import HttpResponse
from django.template.loader import render_to_string
#from weasyprint import HTML

# Create your views here.
@login_required(login_url='/login')
def section_one_view(request,pk):
    context = {
        'customer':get_object_or_404(Customer, pk=pk),
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section1/index.html',context)

@login_required(login_url='/login')
def section_one_document_one_export_pdf(request,pk):
    customers=get_object_or_404(Customer,pk=pk)
    context={
        'customer':customers,
        'user':request.user,
        'agency': Agency.objects.first()
    }
    html_string = render_to_string('pages/customers/actions/sections/section1/pdf_page/page3.html', context)
    html = HTML(string=html_string)
    pdf = html.write_pdf()
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="documento.pdf"'
    return response


@login_required(login_url='/login')
def section_one_document_one_history(request,pk):
    customer=get_object_or_404(Customer, pk=pk)
    context = {
        'documents':HistoricalSection1.objects.filter(customer=customer).order_by('-create_datetime_at'),
        'customer':customer,
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section1/history.html',context)
