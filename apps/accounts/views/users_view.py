from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from apps.accounts.models import User 

# Create your views here.
@login_required(login_url='/login')
def users_view(request):
    context={
        "users":User.objects.all()
    }
    return render(request,'pages/accounts/index.html',context)