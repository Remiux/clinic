from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.symptom.filters import ClientFilter, InsuranceFilter, EncryptedFileFilter
from apps.symptom.form import CustomerForm, CustomerSignForm
from apps.symptom.models import Customer, Diagnostic, Insurance, Symptom
from utils.paginator import _get_paginator 
from apps.symptom.models import Customer
from django.contrib.auth import get_user_model
from apps.symptom.models import EncryptedFile
from apps.symptom.form import FileUploadForm
from django.contrib import messages
from django.shortcuts import redirect

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
def filter_files_view(request):
    files_filter = EncryptedFileFilter(request.GET, queryset=EncryptedFile.objects.all().order_by('created_at'))
    # print(files_filter.qs.query)  # Esto imprimirá la consulta SQL generada
    print(files_filter.qs.query)  # Esto imprimirá la consulta SQL generada
    context = {'files': files_filter.qs}
    return render(request, 'pages/customers/actions/components/partials/files.html', context)


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
    User = get_user_model()
    customer = get_object_or_404(Customer, pk=pk)
    files = EncryptedFile.objects.filter(belongs_to=customer)

    if request.method == 'POST' :
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            file_type = form.cleaned_data['file_type']
            process_start_date = form.cleaned_data['process_start_date']
            EncryptedFile.objects.create(
                file=file,
                file_type=file_type,
                uploaded_by=request.user,
                belongs_to=customer,
                process_start_date=process_start_date
            )
        else:
            # Si el formulario no es válido, mostrar errores
            context = {'customer': customer, 'files': files, 'form': form}
            return render(request, 'pages/customers/actions/detail/customerDetail.html', context)
    else:
        form = FileUploadForm(initial={'belongs_to': customer})

    context = {'customer': customer, 'files': files, 'form': form}
    return render(request, 'pages/customers/actions/detail/customerDetail.html', context)


@login_required(login_url='/login')
def upload_file(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    files = EncryptedFile.objects.filter(belongs_to=customer)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.cleaned_data['file']
            file_type = form.cleaned_data['file_type']
            process_start_date = form.cleaned_data['process_start_date']

            EncryptedFile.objects.create(
                file=file,
                file_type=file_type,
                uploaded_by=request.user,
                belongs_to=customer,
                process_start_date=process_start_date
            )

            if request.headers.get('HX-Request'):
                messages.success(request, 'Archivo subido exitosamente.')
                context = {'files': EncryptedFile.objects.filter(belongs_to=customer)}
                return render(request, 'pages/customers/actions/components/partials/files.html', context)

        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
            if request.headers.get('HX-Request'):
                context = {'customer': customer, 'files': files, 'form': form}
                return render(request, 'pages/customers/actions/components/partials/modal.html', context)

    else:
        form = FileUploadForm(initial={'belongs_to': customer})

    context = {'customer': customer, 'files': files, 'form': form}
    return render(request, 'pages/customers/actions/detail/customerDetail.html', context)


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


