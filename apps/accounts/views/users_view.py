from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
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
    user = get_object_or_404(User,pk=pk)
    context={}
    if user:
        context['user']=user
        context['items']=Group.objects.all()
    return render(request,'pages/accounts/actions/userUpdate.html',context)