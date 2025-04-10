from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.symptom.filters import ClientFilter, InsuranceFilter
from apps.symptom.form import InsuranceForm
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
    customers = Customer.objects.all()
    context = {'customers': customers}
    filtered_context = _show_customers_filter(request)
    context.update(filtered_context)
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
def create_customer_view(request):
    context={
        'diagnostics':Diagnostic.objects.all(),
        'insurances':Insurance.objects.filter(available=True),
    }
    return render(request,'pages/customers/actions/create/customerCreate.html',context)


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
    # Obtener el cliente asociado
    customer = get_object_or_404(Customer, pk=pk)
    files = EncryptedFile.objects.filter(belongs_to=customer)

    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Guardar el archivo y los datos relacionados
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

            # Manejo de solicitudes HTMX
            if request.headers.get('HX-Request'):
                messages.success(request, 'Archivo subido exitosamente.')
                context = {'files': EncryptedFile.objects.filter(belongs_to=customer)}
                return render(request, 'pages/customers/actions/components/partials/files.html', context)

        else:
            # Manejo de errores del formulario
            messages.error(request, 'Por favor corrige los errores en el formulario.')
            if request.headers.get('HX-Request'):
                context = {'customer': customer, 'files': files, 'form': form}
                return render(request, 'pages/customers/actions/components/partials/files.html', context)

            

    else:
        form = FileUploadForm(initial={'belongs_to': customer})

    # Renderizar la página completa si no es una solicitud POST
    context = {'customer': customer, 'files': files, 'form': form}
    return render(request, 'pages/customers/actions/detail/customerDetail.html', context)

# @login_required(login_url='/login')
# def upload_file(request, pk):
#     User = get_user_model()
#     customer = get_object_or_404(Customer, pk=pk)
#     files = EncryptedFile.objects.filter(belongs_to=customer)

#     if request.method == 'POST':
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = form.cleaned_data['file']
#             file_type = form.cleaned_data['file_type']
#             process_start_date = form.cleaned_data['process_start_date']
#             EncryptedFile.objects.create(
#                 file=file,
#                 file_type=file_type,
#                 uploaded_by=request.user,
#                 belongs_to=customer,
#                 process_start_date=process_start_date
#             )
#             print('is valid')
#             context = {'customer': customer, 'files': files, 'form': form}
#             return render(request, 'pages/customers/actions/components/partials/files.html', context)
#         else:
#             # Si el formulario no es válido, mostrar errores
#             print('not valid')
#             context = {'customer': customer, 'files': files, 'form': form}
#             return render(request, 'pages/customers/actions/detail/customerDetail.html', context)
#     else:
#         form = FileUploadForm(initial={'belongs_to': customer})

    # context = {'customer': customer, 'files': files, 'form': form}
    # return render(request, 'pages/customers/actions/detail/customerDetail.html', context)


# def upload_file(request, pk):
#     User = get_user_model()
#     customer = get_object_or_404(Customer, pk=pk)
#     files = EncryptedFile.objects.filter(belongs_to=customer)
#     if request.method == 'POST':
#         form = FileUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = form.cleaned_data['file']
#             file_type = form.cleaned_data['file_type']
#             process_start_date = form.cleaned_data['process_start_date']
#             EncryptedFile.objects.create(
#                 file=file,
#                 file_type=file_type,
#                 uploaded_by=request.user,
#                 belongs_to=customer,
#                 process_start_date=process_start_date
#             )
#             print('File uploaded successfully')
#             messages.success(request, 'Tu perfil ha sido actualizado con éxito.')
#             if request.headers.get('HX-Request'):
#                 print('HTMX')
#                 context = {'files': EncryptedFile.objects.filter(belongs_to=customer)}
#                 return render(request, 'pages/customers/actions/components/partials/files.html', context)
#         else:
#             messages.error(request, 'Por favor corrige los errores a continuación.')
#             print('Im in')
#             context = {'customer': customer, 'files': files, 'form': form}
#             if request.headers.get('HX-Request'):
#                 return render(request, 'pages/customers/actions/components/partials/files.html', context)
                

@login_required(login_url='/login')
def sign_customer_view(request, pk):
    context={}
    return render(request, 'pages/customers/actions/detail/customerGenerateSign.html', context)