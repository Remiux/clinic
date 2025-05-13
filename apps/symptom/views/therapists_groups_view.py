from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from apps.accounts.models import User
from apps.symptom.filters import TherapistsGroupsFilter, GroupsPSRSectionsFilter
from apps.symptom.form import GroupCustomerForm, TherapistsGroupsForm, NoteForm
from apps.symptom.models import Customer, GroupCustomer, TherapistsGroups, GroupsPSRSections, Goal, Objective
from utils.paginator import _get_paginator


# Create your views here.
@login_required(login_url='/login')
def therapists_groups_view(request):
    context = _show_therapists_groups_filter(request)
    context['therapists'] = User.objects.filter(groups__name='therapist').order_by('first_name')
    return render(request,'pages/therapistsGroup/index.html',context)


@login_required(login_url='/login')
def therapists_sections_groups_view(request):
    context = _show_psrSections_filter(request)
    context['therapists'] = User.objects.filter(groups__name='therapist').order_by('first_name')
    context['GroupsPSRSections'] = GroupsPSRSections.objects.filter(is_active=False)
    
    return render(request,'pages/sections_successfully/psr_sections/index.html',context)


def _show_psrSections_filter(request):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    PSRSections = GroupsPSRSectionsFilter(request.GET, queryset=GroupsPSRSections.objects.filter(is_active=False).order_by('-init_hour'))
    context = _get_paginator(request, PSRSections.qs)
    context['parameters'] = parameters
    return context

from datetime import time
from apps.symptom.models import Master, FocusArea, Note

def create_psr_notes_view(request, pk):
    psrSection = get_object_or_404(GroupsPSRSections, pk=pk)
    psrSectionsOnDate = GroupsPSRSections.objects.filter(create_at=psrSection.create_at)
    note = Note.objects.create()
    
    # a cada elemento de psrSectionsOnDate asignarle la nota creada
    for item in psrSectionsOnDate:
        item.note = note
        item.save()
    
    
    context = _show_psrSections_filter(request)
    context['therapists'] = User.objects.filter(groups__name='therapist').order_by('first_name')
    context['GroupsPSRSections'] = GroupsPSRSections.objects.filter(is_active=False)
    
    return render(request,'pages/sections_successfully/psr_sections/partials/psrSectionTable.html',context)
    

def update_psr_notes_view(request, pk, date):
    #init_hour__lte=time(13, 5)    
    psrSections = GroupsPSRSections.objects.filter(create_at=date, is_active=False).order_by('init_hour')
    customer = get_object_or_404(Customer, pk=pk)
    note = psrSections.first().note if psrSections.exists() else None
    
    # Obtener los Goals asociados al Customer
    goals = Goal.objects.filter(focus_area__master__customer=customer)
    
    # Obtener los Objectives asociados a los Goals
    objectives = Objective.objects.filter(goal__in=goals)
    
    
    # Pasar los datos al contexto
    context = {
        'psrSections': psrSections,
        'customer': customer,
        'goals': goals,
        'objectives': objectives,
        'note': note,
    }
    
    return render(request, 'pages/sections_successfully/psr_sections/update_note.html', context)
    
    
def save_note_changes(request, pk):
    psrSection = get_object_or_404(GroupsPSRSections, pk=pk)
    note = psrSection.note
    
    context = {}
    form = NoteForm(request.POST or None, instance=note)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            context['tags']="success"
            context['tag_messsage']="Changes saved successfully!"
        else:
            print(form.errors)
            context['tags']="error"
            context['tag_messsage']="Something went wrong!"
    
    context['form'] = form
    return render(request,'pages/sections_successfully/psr_sections/partials/notes.html', context)


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
                context['create_messsage']="Create customer successfully"
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