from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from apps.accounts.forms.user_form import UpdateForm
from apps.accounts.models import User 

# Create your views here.
@login_required(login_url='/login')
def users_view(request):
    context={
        "users":User.objects.all()
    }
    return render(request,'pages/accounts/index.html',context)

@login_required(login_url='/login')
def detail_user_view(request,pk):
    user = get_object_or_404(User,pk=pk)
    
    context={}
    if user:
        context['user']=user
    return render(request,'pages/accounts/actions/userDetail.html',context)

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