from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from apps.accounts.filters import UserFilter
from apps.accounts.forms.user_form import CreateForm, ProfileUpdateForm, UpdateForm
from apps.accounts.models import User
from apps.symptom.models import Customer, EncryptedFileUser
from utils.paginator import _get_paginator 
from django.contrib.auth.forms import PasswordChangeForm
from apps.symptom.filters import EncryptedFileFilter, EncryptedFileFilterUser
from apps.symptom.form import FileUploadForm, FileUploadFormUser
from utils.file_extension import get_file_extension
from apps.symptom.utils import encrypt_file, decrypt_file
from django.http import HttpResponse
from django.template.loader import render_to_string

# Create your views here.
@login_required(login_url='/login')
def users_view(request):
    context=_show_user_filter(request)
    context['groups']=Group.objects.all()
    return render(request,'pages/accounts/index.html',context)


def create_user_view(request):
    form = CreateForm(request.POST or None)
    context={
        'groups':Group.objects.all(),
    }
    if request.method == "POST":
        if form.is_valid():
            form.save()
            form.save_m2m()
            context['message']='Successfull'
            form=CreateForm()
        else:
            pass
    context['form']=form
    return render(request,'pages/accounts/actions/form/userFormCreate.html',context)


@login_required(login_url='/login')
def filter_users_view(request):
    context=_show_user_filter(request)
    return render(request,'pages/accounts/userTable.html',context)

@login_required(login_url='/login')
def detail_user_view(request,pk):
    user = get_object_or_404(User,pk=pk)
    context = _show_files_filter(request, pk)
    
    if user:
        context['user']=user
    return render(request,'pages/accounts/actions/userDetail.html',context)

@login_required(login_url='/login')
def filter_files_user_view(request, pk):
    context = _show_files_filter(request, pk)
    return render(request, 'pages/accounts/actions/partials/files.html', context)


def _show_files_filter(request, pk):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    files = EncryptedFileFilterUser(request.GET, queryset=EncryptedFileUser.objects.filter(belongs_to=pk).order_by('-id'))
    context = _get_paginator(request, files.qs)
    context['user'] = get_object_or_404(User, pk=pk)
    context['parameters'] = parameters
    return context


def _show_user_filter(request):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    users = UserFilter(request.GET, queryset=User.objects.all().order_by('id'))
    context = _get_paginator(request, users.qs)
    context['parameters'] = parameters
    return context

@login_required(login_url='/login')
def update_user_view(request,pk):
    import base64
    from django.core.files.base import ContentFile
    user = get_object_or_404(User,pk=pk)
    form = UpdateForm(request.POST or None,instance =user)
    context={}
    
    if user:

        if request.method == 'POST':
            signature_data = request.POST.get('sign','')
            form = UpdateForm(request.POST,request.FILES,instance =user)
            if form.is_valid():
                profile = form.save(commit=False)
                if signature_data:
                    # Extraer los datos base64 del Data URL
                    format, imgstr = signature_data.split(';base64,') 
                    ext = format.split('/')[-1]  # 'png'
                    # Crear archivo
                    file_name = f"signature_{user.pk}.{ext}"
                    file_content = ContentFile(base64.b64decode(imgstr), name=file_name)
                    
                    # Guardar en el modelo
                    profile.sign.save(file_name, file_content, save=True)
                profile.is_active=True if request.POST.get('is_active','') else False
                profile.save() 
                form.save_m2m()
                context['message']="User updated successfully"
            else:
                pass
        context['user']=user
        context['items']=Group.objects.all()
        context['form']=form
    return render(request,'pages/accounts/actions/userUpdate.html',context)


@login_required(login_url='/login')
def change_password_view(request):
    form = PasswordChangeForm(request.user)
    context={}
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            pass
    context['form']=form
    return render(request,'pages/accounts/actions/changePassword.html',context)



@login_required(login_url='/login')
def user_profile_view(request):
    form = ProfileUpdateForm(instance=request.user)
    context={}
    if request.method == 'POST':
        form = ProfileUpdateForm( request.POST,instance=request.user)
        if form.is_valid():
            form.save()
        else:
            pass
    context['form']=form
    context['user']=request.user
    return render(request,'pages/accounts/actions/userProfile.html',context)


"""
|--------------------------|
 File Management for Users |
|--------------------------|
"""



@login_required(login_url='/login')
def upload_file_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    context = {}
    if request.method == 'POST':
        form = FileUploadFormUser(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.uploaded_by = request.user
            document.belongs_to = user
            document.file_type = get_file_extension(request.FILES.get('file'))
            # Leer y encriptar el archivo
            file = request.FILES.get('file')
            encrypted_data = encrypt_file(file.read())
            # Asignar el archivo encriptado al campo correspondiente
            document.encrypted_file = encrypted_data
            
            document.save()
            
            
            context['tags'] = 'success'
            context['tag_message'] = 'File uploaded successfully!'
            context['message'] = 'File uploaded successfully!'
        else:
            context['tags'] = 'error'
            context['tag_message'] = 'Error uploading file!'
        
    context['user'] = user
    context['form'] = form
    
    
    return render(request, 'pages/accounts/actions/partials/modal_form.html', context)


@login_required(login_url='/login')
def delete_file_user_view(request, pk):
    try:
        file = get_object_or_404(EncryptedFileUser, pk=pk)
        user = file.belongs_to  
        file.delete()  

        # Renderizar la plantilla actualizada
        context = _show_files_filter(request, user.pk)
        context['tags'] = 'success'
        context['tag_message'] = 'File deleted successfully!'
        context['message'] = 'File deleted successfully!'
        html = render_to_string('pages/accounts/actions/partials/files.html', context)
        return HttpResponse(html, status=200)
    except Exception as e:
        # Renderizar la plantilla con un mensaje de error
        context = _show_files_filter(request, file.belongs_to.pk)
        context['tags'] = 'error'
        context['tag_message'] = 'Error deleting file!'
        html = render_to_string('pages/accounts/actions/partials/files.html', context)
        return HttpResponse(html, status=400)