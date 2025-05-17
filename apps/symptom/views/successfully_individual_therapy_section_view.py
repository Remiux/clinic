from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.accounts.models import User
from apps.symptom.filters import IndividualTherapySectionFilter, InsuranceFilter
from apps.symptom.form import IndividualTherapySectionNoteForm, InsuranceForm, SignIndividualTherapySectionNoteForm
from apps.symptom.models import Customer, Goal, GoalNoteIndividualTherapySections, IndividualTherapySection, IndividualTherapySectionNote, Insurance, Objective, ObjectiveNoteIndividualTherapySections, Symptom
from utils.paginator import _get_paginator 
from django.utils import timezone

# Create your views here.
@login_required(login_url='/login')
def successfully_individual_therapy_section_view(request):
    context=_show_successfully_individual_therapy_section_filter(request)
    context['customers'] = Customer.objects.all().order_by('first_name')
    return render(request,'pages/sections_successfully/individual_therapy_section/index.html',context)



@login_required(login_url='/login')
def filter_successfully_individual_therapy_section_view(request):
    context=_show_successfully_individual_therapy_section_filter(request)
    return render(request,'pages/sections_successfully/individual_therapy_section/individualTherapySectionTable.html',context)


def _show_successfully_individual_therapy_section_filter(request):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    insurance = IndividualTherapySectionFilter(request.GET, queryset=IndividualTherapySection.objects.filter(is_active=False).order_by('-pk'))
    context = _get_paginator(request, insurance.qs)
    context['parameters'] = parameters
    return context



@login_required(login_url='/login')
def detail_successfully_individual_therapy_view(request,pk):
    individual_therapy = get_object_or_404(IndividualTherapySection,pk=pk,is_active=False)
    goals = Goal.objects.filter(focus_area__master__customer = individual_therapy.customer.pk, focus_area__master__is_active = False,focus_area__focus_area_type = 'Individual' )
    individual_note = IndividualTherapySectionNote.objects.filter(
        individual_therapy_section = individual_therapy
    ).first()
    therapist = User.objects.filter(pk=individual_therapy.therapist_pk).first()
    if not individual_note:
        individual_note = IndividualTherapySectionNote.objects.create(
            individual_therapy_section = individual_therapy,
            therapist = User.objects.get(pk= individual_therapy.therapist_pk)
        )
    goals_note = GoalNoteIndividualTherapySections.objects.filter(individual_note = individual_note)
    context={
        'individual_therapy' : individual_therapy,
        'goals': goals,
        'individual_note':individual_note,
        'goals_note':goals_note,
        'therapist':therapist
    }
    return render(request,'pages/sections_successfully/individual_therapy_section/actions/individualTherapySectionDetail.html',context)


@login_required(login_url='/login')
def add_goal_individual_therapy_note_view(request,pk,goal):
    individual_therapy = get_object_or_404(IndividualTherapySection,pk=pk,is_active=False)
    goal = get_object_or_404(Goal,pk=goal)
    exist = False
    individual_note = IndividualTherapySectionNote.objects.get(individual_therapy_section = individual_therapy)
    if not GoalNoteIndividualTherapySections.objects.filter(individual_note= individual_note,goal_title = goal.title).exists():
        goal_note = GoalNoteIndividualTherapySections.objects.create(
            individual_note = individual_note,
            goal_number = goal.focus_area.number,
            goal_title = goal.title
        )
        for objective in Objective.objects.filter(goal = goal):
            ObjectiveNoteIndividualTherapySections.objects.create(
                goal_note=goal_note,
                objective_number = objective.number,
                objective_description = objective.description
                
            )
    else:
        exist = True
    individual_note = IndividualTherapySectionNote.objects.get(
        individual_therapy_section = individual_therapy
    )
    context={
        'individual_therapy' : individual_therapy,
        'goals_note': GoalNoteIndividualTherapySections.objects.filter(individual_note = individual_note).order_by('goal_number'),
        'message': 'This goal is in this note' if exist else 'Add goal successfully',
        'tags': 'error' if  exist else 'success' ,

    }
    return render(request,'pages/sections_successfully/individual_therapy_section/partials/goalsAndObjctiveList.html',context)



@login_required(login_url='/login')
def delete_goal_individual_therapy_note_view(request, pk):
    goal_note = get_object_or_404(GoalNoteIndividualTherapySections,pk=pk)
    context = {'goal_note':goal_note} 
    if request.method == 'DELETE':
        if goal_note:
            goal_note.delete()
            context['message']="Remove goal successfully"
            context['tags']="success"
            context['goal_note']=[]
    return render(request, 'pages/sections_successfully/individual_therapy_section/partials/goalAndObjectiveCard.html', context)

@login_required(login_url='/login')
def delete_objective_goal_individual_therapy_note_view(request, pk):
    objective_goal_note = get_object_or_404(ObjectiveNoteIndividualTherapySections,pk=pk)
    context = {'goal_note':objective_goal_note.goal_note} 
    if request.method == 'DELETE':
        if objective_goal_note:
            objective_goal_note.delete()
            context['message']="Remove objective successfully"
            context['tags']="success"
            
    return render(request, 'pages/sections_successfully/individual_therapy_section/partials/goalAndObjectiveCard.html', context)


@login_required(login_url='/login')
def sign_individual_note_view(request, pk):
    import base64
    from django.core.files.base import ContentFile
    individual_note=get_object_or_404(IndividualTherapySectionNote, pk=pk)
    
    context={
        'individual_note':individual_note,
    }
    if request.method == 'POST':
        form = SignIndividualTherapySectionNoteForm(request.POST, request.FILES, instance=individual_note)
        signature_data = request.POST.get('sign','')
        
        if form.is_valid():
            individual_note_update=form.save(commit=False)
            
            if signature_data:
                    # Extraer los datos base64 del Data URL
                    format, imgstr = signature_data.split(';base64,') 
                    ext = format.split('/')[-1]  # 'png'
                    # Crear archivo
                    file_name = f"individualTherapy_note_licensed_signature_{individual_note.pk}.{ext}"
                    file_content = ContentFile(base64.b64decode(imgstr), name=file_name)
                    
                    # Guardar en el modelo
                    individual_note_update.sign.save(file_name, file_content, save=True)
            individual_note_update.date_sign = timezone.now()
            individual_note_update.licensed_practitioner = f"{request.user.first_name} {request.user.last_name}"
            individual_note_update.licensed_practitioner_pk = request.user.pk
            individual_note_update.save()
            context['message'] = 'Sign updated successfully'
            context['tags'] = 'success'
    return render(request, 'pages/sections_successfully/individual_therapy_section/partials/LicencsedPractitionerSignature.html', context)



@login_required(login_url='/login')
def update_individual_therapy_section_view(request, pk):
    individual_note = get_object_or_404(IndividualTherapySectionNote,pk=pk)
    context = {'individual_note':individual_note} 
    if request.method == 'POST':
        form = IndividualTherapySectionNoteForm(request.POST, instance=individual_note)
        if form.is_valid():
            form.save()
            print('asere')
        else:
            print(form.errors)
        if individual_note:
            context['message']="Change successfully"
            context['tags']="success"
            
    return render(request, 'pages/sections_successfully/individual_therapy_section/partials/confirm.html', context)
