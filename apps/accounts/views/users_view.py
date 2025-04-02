from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from apps.accounts.filters import UserFilter
from apps.accounts.forms.user_form import CreateForm, UpdateForm
from apps.accounts.models import User
from utils.paginator import _get_paginator 

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
    return render(request,'cotton/userTable.html',context)

@login_required(login_url='/login')
def detail_user_view(request,pk):
    user = get_object_or_404(User,pk=pk)
    
    context={}
    if user:
        context['user']=user
    return render(request,'pages/accounts/actions/userDetail.html',context)

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
                context['message']="Update user successfull"
            else:
                pass
        context['user']=user
        context['items']=Group.objects.all()
        context['form']=form
    return render(request,'pages/accounts/actions/userUpdate.html',context)