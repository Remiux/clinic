from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from apps.accounts.models import User
from apps.symptom.filters import TherapistsGroupsFilter
from apps.symptom.form import GroupCustomerForm, TherapistsGroupsForm
from apps.symptom.models import Customer, GroupCustomer, TherapistsGroups
from utils.paginator import _get_paginator


# Create your views here.
@login_required(login_url='/login')
def therapists_groups_view(request):
    context = _show_therapists_groups_filter(request)
    context['therapists'] = User.objects.filter(groups__name='therapist').order_by('first_name')
    return render(request,'pages/therapistsGroup/index.html',context)


@login_required(login_url='/login')
def filter_therapists_groups_view(request):
    context=_show_therapists_groups_filter(request)
    return render(request,'pages/therapistsGroup/GroupsCardList.html',context)

def _show_therapists_groups_filter(request):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    customers = TherapistsGroupsFilter(request.GET, queryset=TherapistsGroups.objects.all().order_by('-pk'))
    context = _get_paginator(request, customers.qs)
    context['parameters'] = parameters
    return context



@login_required(login_url='/login')
def detail_therapists_groups_view(request, pk):
    context = {'group':get_object_or_404(TherapistsGroups, pk=pk)} 
    context['customers'] = Customer.objects.all().order_by('case_no')
    context['therapists'] = User.objects.filter(groups__name='therapist').order_by('first_name')
    return render(request, 'pages/therapistsGroup/actions/detail/GroupDetail.html', context)

@login_required(login_url='/login')
def create_group_view(request):
    form = TherapistsGroupsForm(request.POST or None)
    if request.method == 'POST':
        form = TherapistsGroupsForm(request.POST)
        if form.is_valid():
            form = form.save() 
    context = _show_therapists_groups_filter(request)
    return render(request, 'pages/therapistsGroup/GroupsCardList.html', context)

@login_required(login_url='/login')
def create_customer_group_view(request, pk):
    group = get_object_or_404(TherapistsGroups, pk=pk)
    context = {'group':group} 
    if request.method == 'POST':
        form = GroupCustomerForm(request.POST)
        if GroupCustomer.objects.filter(group=group,customer=Customer.objects.get(pk=request.POST['customer'])).exists():
            context['create_messsage']="The customer is listed"
            context['tags']="error"
        else:  
            if form.is_valid():
                customer = form.save(commit=False)
                customer.group = group
                customer.save()
                context['create_messsage']="Create customer successfull"
                context['tags']="success"
    return render(request, 'pages/therapistsGroup/components/customerGroupList.html', context)

@login_required(login_url='/login')
def update_therapist_group_view(request, pk):
    group = get_object_or_404(TherapistsGroups, pk=pk)
    context = {'group':group} 
    if request.method == 'POST':
        therapist = get_object_or_404(User, pk=request.POST.get('therapist'))
        group.therapist = therapist
        group.save()
    return render(request, 'pages/therapistsGroup/components/updateTherapistGroupPerfil.html', context)

@login_required(login_url='/login')
def update_service_group_view(request, pk):
    group = get_object_or_404(TherapistsGroups, pk=pk)
    context = {'group':group} 
    if request.method == 'POST':
        if group.type == True:
            group.type = False
        else:
            group.type = True
        group.save()
    return render(request, 'pages/therapistsGroup/components/updateServiceGroupPerfil.html', context)

@login_required(login_url='/login')
def update_active_service_group_view(request, pk):
    customer = get_object_or_404(GroupCustomer, pk=pk)
    context = {'customer':customer} 
    if request.method == 'POST':
        if customer.is_active == True:
            customer.is_active = False
        else:
            customer.is_active = True
        customer.save()
    return render(request, 'pages/therapistsGroup/components/customerGroupCard.html', context)

@login_required(login_url='/login')
def delete_customer_group_view(request, pk):
    customer = get_object_or_404(GroupCustomer, pk=pk)
    context = {'customer':customer} 
    if request.method == 'DELETE':
        if customer:
            customer.delete()
            context['message']="Deleted customer successfull"
            context['tags']="success"
            context['customer']=[]
    return render(request, 'pages/therapistsGroup/components/customerGroupCard.html', context)