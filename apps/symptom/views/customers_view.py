from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.symptom.filters import ClientFilter, InsuranceFilter, EncryptedFileFilter
from apps.symptom.form import CustomerForm, CustomerSignForm
from apps.symptom.models import Customer, Diagnostic, Insurance, Symptom, Eligibility, Therapist, PsychiatricEvaluation
from utils.paginator import _get_paginator
from utils.file_extension import get_file_extension
from apps.symptom.models import Customer
from django.contrib.auth import get_user_model
from apps.symptom.models import EncryptedFile
from apps.symptom.form import FileUploadForm
from django.contrib import messages
from django.shortcuts import redirect
from apps.symptom.utils import encrypt_file, decrypt_file
from django.http import HttpResponse
from django.template.loader import render_to_string

# Create your views here.
@login_required(login_url='/login')
def customers_view(request):
    context = _show_customers_filter(request)
    context['diagnostics'] = Diagnostic.objects.all()
    return render(request,'pages/customers/index.html',context)


@login_required(login_url='/login')
def filter_customers_view(request):
    context=_show_customers_filter(request)
    return render(request,'pages/customers/customerCardList.html',context)


def _show_customers_filter(request):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    customers = ClientFilter(request.GET, queryset=Customer.objects.all().order_by('case_no'))
    context = _get_paginator(request, customers.qs)
    context['parameters'] = parameters
    return context


@login_required(login_url='/login')
def filter_files_view(request, pk):
    context = _show_files_filter(request, pk)
    return render(request, 'pages/customers/actions/components/partials/files.html', context)

def _show_files_filter(request, pk):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    files = EncryptedFileFilter(request.GET, queryset=EncryptedFile.objects.filter(belongs_to=pk).order_by('-id'))
    context = _get_paginator(request, files.qs)
    context['customer'] = get_object_or_404(Customer, pk=pk)
    context['parameters'] = parameters
    return context


@login_required(login_url='/login')
def create_customer_view(request):
    form = CustomerForm()
    context={
        'diagnostics':Diagnostic.objects.all().order_by('code'),
        'insurances':Insurance.objects.filter(available=True).order_by('name'),
    }
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
           form.save()
           context['message'] = 'Customer created successfully'
        else:
            print(form.errors)
    context['form'] = form
    return render(request,'pages/customers/actions/create/customerCreate.html',context)

@login_required(login_url='/login')
def update_customer_view(request,pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = CustomerForm(instance=customer)
    context={
        'diagnostics':Diagnostic.objects.all().order_by('code'),
        'insurances':Insurance.objects.filter(available=True).order_by('name'),
        'customer':customer,
    }
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
           form.save()
           context['message'] = 'Customer update successfully'
        else:
            print(form.errors)
    context['form'] = form
    return render(request,'pages/customers/actions/update/customerUpdate.html',context)

@login_required(login_url='/login')
def detail_customer_view(request, pk):
    context = _show_files_filter(request, pk)
    context['customer'] = get_object_or_404(Customer, pk=pk)
    return render(request, 'pages/customers/actions/detail/customerDetail.html', context)


@login_required(login_url='/login')
def upload_file(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    context = {}
    flag = False
    option = 0
    if 'procedence' in request.POST:
        option = 2
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.belongs_to = customer
            document.file_type = get_file_extension(request.FILES.get('file'))
            # Leer y encriptar el archivo
            file = request.FILES.get('file')
            encrypted_data = encrypt_file(file.read())
            # Asignar el archivo encriptado al campo correspondiente
            document.encrypted_file = encrypted_data
            
            document.save()
            
            # Crear instancia de Eligibility si el nombre del archivo es 'eligibility' o 'Eligibility' y el tipo de archivo es '.pdf'
            file_name = file.name
            if (file_name.lower() == 'elegibility' or file_name.lower() == 'elegibility.pdf'):
                Eligibility.objects.create(
                    encrypted_file=document,
                    description="Elegibility document uploaded."
                )
                option = 1
            elif (file_name.lower() == 'psychiatric_evaluation' or file_name.lower() == 'psychiatric_evaluation.pdf'):
                flag = True
                therapist_pk = request.POST.get('therapist')
                procedence = request.POST.get('procedence')
                therapist = Therapist.objects.filter(pk=therapist_pk).first()
                PsychiatricEvaluation.objects.create(
                    encrypted_file=document,
                    procedence=procedence,
                    therapist=therapist,
                )
                option = 2
            
            context['tags'] = 'success'
            context['tag_message'] = 'File uploaded successfully!'
            context['message'] = 'File uploaded successfully!'
            
        else:
            context['tags'] = 'error'
            context['tag_message'] = 'Error uploading file!'
        
    context['customer'] = customer
    context['form'] = form
    print(option)
    if not flag and option == 0:
        return render(request, 'pages/customers/actions/components/partials/modal_form.html', context)
    else:
        context['therapists'] = Therapist.objects.all()
        return render(request, 'pages/customers/actions/sections/section3/partials/modal_form.html', context)

@login_required(login_url='/login')
def delete_file_view(request, pk):
    try:
        file = get_object_or_404(EncryptedFile, pk=pk)
        customer = file.belongs_to  
        file.delete()  

        # Renderizar la plantilla actualizada
        context = _show_files_filter(request, customer.pk)
        context['tags'] = 'success'
        context['tag_message'] = 'File deleted successfully!'
        context['message'] = 'File deleted successfully!'
        html = render_to_string('pages/customers/actions/components/partials/files.html', context)
        return HttpResponse(html, status=200)
    except Exception as e:
        # Renderizar la plantilla con un mensaje de error
        context = _show_files_filter(request, file.belongs_to.pk)
        context['tags'] = 'error'
        context['tag_message'] = 'Error deleting file!'
        html = render_to_string('pages/customers/actions/components/partials/files.html', context)
        return HttpResponse(html, status=400)
    
    
@login_required(login_url='/login')
def delete_elegibility_file_view(request, pk):
    try:
        file = get_object_or_404(EncryptedFile, pk=pk)
        customer = file.belongs_to  
        file.delete()  

        # Renderizar la plantilla actualizada
        context = _show_files_filter(request, customer.pk)
        context['tags'] = 'success'
        context['tag_message'] = 'File deleted successfully!'
        context['message'] = 'File deleted successfully!'
        context['elegibilities'] = Eligibility.objects.filter(encrypted_file__belongs_to=customer.pk).order_by('-created_at')
        html = render_to_string('pages/customers/actions/sections/section2/partials/timeline.html', context)
        return HttpResponse(html, status=200)
    except Exception as e:
        # Renderizar la plantilla con un mensaje de error
        context = _show_files_filter(request, file.belongs_to.pk)
        context['tags'] = 'error'
        context['tag_message'] = 'Error deleting file!'
        context['elegibilities'] = Eligibility.objects.filter(encrypted_file__belongs_to=customer.pk).order_by('-created_at')
        html = render_to_string('pages/customers/actions/sections/section2/partials/timeline.html', context)
        return HttpResponse(html, status=400)


@login_required(login_url='/login')
def delete_psichiatric_evaluation_file_view(request, pk):
    try:
        file = get_object_or_404(EncryptedFile, pk=pk)
        customer = file.belongs_to  
        file.delete()  

        # Renderizar la plantilla actualizada
        context = _show_files_filter(request, customer.pk)
        context['tags'] = 'success'
        context['tag_message'] = 'File deleted successfully!'
        context['message'] = 'File deleted successfully!'
        context['psichiatric_evaluations'] = PsychiatricEvaluation.objects.filter(encrypted_file__belongs_to=customer.pk).order_by('-encrypted_file__created_at')
        html = render_to_string('pages/customers/actions/sections/section3/partials/timeline.html', context)
        return HttpResponse(html, status=200)
    except Exception as e:
        # Renderizar la plantilla con un mensaje de error
        context = _show_files_filter(request, file.belongs_to.pk)
        context['tags'] = 'error'
        context['tag_message'] = 'Error deleting file!'
        #context['elegibilities'] = Eligibility.objects.filter(encrypted_file__belongs_to=customer.pk).order_by('-created_at')
        context['psichiatric_evaluations'] = PsychiatricEvaluation.objects.filter(encrypted_file__belongs_to=customer.pk).order_by('-encrypted_file__created_at')
        html = render_to_string('pages/customers/actions/sections/section3/partials/timeline.html', context)
        return HttpResponse(html, status=400)

@login_required(login_url='/login')
def sign_customer_view(request, pk):
    import base64
    from django.core.files.base import ContentFile
    customer=get_object_or_404(Customer, pk=pk)
    form = CustomerSignForm(instance=customer)
    context={
        'customer':customer,
        'form':form,
    }
    if request.method == 'POST':
        form = CustomerSignForm(request.POST, request.FILES, instance=customer)
        signature_data = request.POST.get('sign','')
        if form.is_valid():
            customer=form.save(commit=False)
            if signature_data:
                    # Extraer los datos base64 del Data URL
                    format, imgstr = signature_data.split(';base64,') 
                    ext = format.split('/')[-1]  # 'png'
                    # Crear archivo
                    file_name = f"signature_{customer.pk}.{ext}"
                    file_content = ContentFile(base64.b64decode(imgstr), name=file_name)
                    
                    # Guardar en el modelo
                    customer.sign.save(file_name, file_content, save=True)
            customer.save()
            context['message'] = 'Customer sign updated successfully'
    return render(request, 'pages/customers/actions/detail/customerGenerateSign.html', context)


