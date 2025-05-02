from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from apps.accounts.models import User
from apps.symptom.filters import IndividualTherapyFilter
from apps.symptom.form import GroupCustomerForm, IndividualTherapyForm, TherapistsGroupsForm
from apps.symptom.models import Customer, IndividualTherapy, IndividualTherapySection, TherapistsGroups
from utils.hours import individual_therapy_dateValues
from utils.paginator import _get_paginator


# Create your views here.
@login_required(login_url='/login')
def individual_terapy_view(request):
    context = _show_individual_terapy_filter(request)
    context['therapists'] = User.objects.filter(groups__name='therapist',is_master=True).order_by('first_name')
    context['customers'] = Customer.objects.all().order_by('first_name')
    return render(request,'pages/indivualTherapy/index.html',context)


@login_required(login_url='/login')
def filter_individual_therapy_view(request):
    context=_show_individual_terapy_filter(request)
    return render(request,'pages/indivualTherapy/GroupsCardList.html',context)

def _show_individual_terapy_filter(request):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    individual_therapies = IndividualTherapyFilter(request.GET, queryset=IndividualTherapy.objects.all().order_by('therapist'))
    context = _get_paginator(request, individual_therapies.qs)
    context['parameters'] = parameters
    return context



@login_required(login_url='/login')
def create_individual_therapy_view(request):
    form = IndividualTherapyForm(request.POST or None)
    error=''
    if request.method == 'POST':
        form = IndividualTherapyForm(request.POST)
        therapist = User.objects.filter(pk=request.POST['therapist']).first()
        if form.is_valid():
            individual_therapy = form.save(commit=False)
            groups=therapist.therapist_group.all()
            if groups.exists():
                for group in groups:
                    if group.type:
                        individual_therapy.type=False
                    else:
                        individual_therapy.type=True
                    break
            individual_therapy.save()
        else:
            error = "The client already belongs to an individual therapy."
    context = _show_individual_terapy_filter(request)
    if error:
        context['error']= error
        context['tags']="error"
    return render(request, 'pages/indivualTherapy/GroupsCardList.html', context)


@login_required(login_url='/login')
def detail_individual_therapy_view(request,pk):
    individual_therapy = get_object_or_404(IndividualTherapy, pk=pk)
    context = {'individual_therapy':individual_therapy} 
    context['therapists'] =  User.objects.filter(groups__name='therapist',is_master=True).order_by('first_name')
    context['sections'] = IndividualTherapySection.objects.filter(is_active=True,individual_therapy_pk=pk)
    context['dateValues']=individual_therapy_dateValues(individual_therapy)
    return render(request, 'pages/indivualTherapy/actions/detail/GroupDetail.html', context)


@login_required(login_url='/login')
def update_therapist_individual_therapy_view(request, pk):
    individual_therapy = get_object_or_404(IndividualTherapy, pk=pk)
    context = {'individual_therapy':individual_therapy} 
    if request.method == 'POST':
        therapist = get_object_or_404(User, pk=request.POST.get('therapist'))
        individual_therapy.therapist = therapist
        individual_therapy.save()
    return render(request, 'pages/indivualTherapy/components/updateTherapistGroupPerfil.html', context)


@login_required(login_url='/login')
def update_service_individual_therapy_view(request, pk):
    individual_therapy = get_object_or_404(IndividualTherapy, pk=pk)
    context = {'individual_therapy':individual_therapy} 
    if request.method == 'POST':
        if individual_therapy.type == True:
            individual_therapy.type = False
        else:
            individual_therapy.type = True
        individual_therapy.save()
    return render(request, 'pages/indivualTherapy/components/updateServiceGroupPerfil.html', context)


@login_required(login_url='/login')
def create_section_individual_therapy_view(request, pk):
    individual_therapy = get_object_or_404(IndividualTherapy, pk=pk)
    context = {'individual_therapy':individual_therapy} 
    if request.method == 'POST':
        IndividualTherapySection.objects.create(
            individual_therapy_pk=individual_therapy.pk,
            customer=individual_therapy.customer,
            therapist_pk= individual_therapy.therapist.pk,
            therapist_full_name= f"{individual_therapy.therapist.first_name} {individual_therapy.therapist.last_name}"
        )
    return render(request, 'pages/indivualTherapy/components/updateServiceGroupPerfil.html', context)


@login_required(login_url='/login')
def delete_section_individual_therapy_view(request,pk):
    section = get_object_or_404(IndividualTherapySection, pk=pk)
    context = {
        'section':section,
    }
    if request.method == 'DELETE':
        section.delete()
        context['section']=[]
    
    return render(request,'pages/indivualTherapy/components/sectionIndividualTherapyCard.html',context)