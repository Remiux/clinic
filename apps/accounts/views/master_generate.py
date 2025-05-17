from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.filters import MasterGenerateFilter
from apps.accounts.forms.generate_master_form import CreateGenerateMasterForm
from apps.accounts.models import MasterGenerate, User
from apps.symptom.models import Customer, Master
from utils.paginator import _get_paginator 


# Create your views here.
@login_required(login_url='/login')
def generate_master_view(request,pk):
    context=_show_generate_master_filter(request,pk)
    context['user']= get_object_or_404(User,pk=pk)
    context['customers'] = Customer.objects.all().order_by('first_name')
    return render(request,'pages/accounts/generateMaster/index.html',context)



@login_required(login_url='/login')
def filter_generate_master_view(request,pk):
    context=_show_generate_master_filter(request,pk)
    context['user']= get_object_or_404(User,pk=pk)
    return render(request,'pages/accounts/generateMaster/table_result.html',context)



def _show_generate_master_filter(request,pk):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    generate_master = MasterGenerateFilter(request.GET, queryset=MasterGenerate.objects.filter(user=pk).order_by('-id'))
    context = _get_paginator(request, generate_master.qs)
    context['parameters'] = parameters
    return context

@login_required(login_url='/login')
def create_generate_master_view(request,pk):
    user = get_object_or_404(User,pk=pk)
    form = CreateGenerateMasterForm()
    context={
        "customers":Customer.objects.all().order_by('first_name'),
        "user":user
    }
    if user:
        if request.method == "POST":
            form = CreateGenerateMasterForm(request.POST)
            customer = Customer.objects.get(pk = request.POST['customer'])
            if form.is_valid():
                generate_master = form.save(commit=False)
                generate_master.user = user
                customer = customer
                generate_master.customer_pk = customer.pk
                generate_master.customer_full_name = customer.full_name
                Master.objects.create(
                    customer = customer,
                    user = user,
                    date = request.POST.get('generate_date'),
                    start_time = request.POST.get('generate_init_time'),
                    end_time = request.POST.get('generate_end_time'),
                    initial_discharge_criteria=''
                )
                generate_master.save()
                context["message"]="Generate master successfull"
    context['form']=form
    return render(request,'pages/accounts/generateMaster/actions/generateMasterFormCreate.html',context)


@login_required(login_url='/login')
def delete_generate_master_view(request,pk):
    genearate_master = get_object_or_404(MasterGenerate,pk=pk,is_active = True)
    if genearate_master and request.method == "DELETE":
        genearate_master.delete()
        genearate_master = []
    context={
        'master': genearate_master
        } 
    return render(request,'pages/accounts/generateMaster/master.html',context)


