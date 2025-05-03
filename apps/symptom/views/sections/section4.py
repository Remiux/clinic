from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.symptom.models import *
from django.http import HttpResponse
from django.template.loader import render_to_string
from apps.symptom.form import *
from utils.file_extension import get_file_extension
from apps.symptom.utils import encrypt_file, decrypt_file
from django.views.decorators.http import require_POST


@login_required(login_url='/login')
def section_four_view(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    
    # Verificar si el cliente está asociado a alguna IndividualTherapy
    is_in_individual_therapy = IndividualTherapy.objects.filter(customer=customer).exists()
    
    # Verificar si el cliente está asociado a algún GroupCustomer
    is_in_group_customer = GroupCustomer.objects.filter(customer=customer).exists()
    
    focus_areas = FocusArea.objects.prefetch_related('goal_set__objective_set', 'goal_set__intervention_set')
    context = {
        'customer': customer,
        'agency': Agency.objects.first(),
        'is_in_individual_therapy': is_in_individual_therapy,
        'is_in_group_customer': is_in_group_customer,
        'focus_areas': focus_areas,
        'goal_form': GoalForm(),
        'objective_form': ObjectiveForm(),
        'intervention_form': InterventionForm(),
    }
    return render(request, 'pages/customers/actions/sections/section4/index.html', context)

def reload_data(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    focus_areas = FocusArea.objects.prefetch_related('goal_set__objective_set', 'goal_set__intervention_set')
    
    context = {
        'customer': customer,
        'focus_areas': focus_areas,
        'goal_form': GoalForm(),
        'objective_form': ObjectiveForm(),
        'intervention_form': InterventionForm(),
    }
    
    return render(request, 'pages/forms/section4/partials/focus_area.html', context)
    


@login_required(login_url='/login')
def section_four_document_suicida_risk_history(request,pk):
    customer=get_object_or_404(Customer, pk=pk)     
    context = {
        'suicide_risks': SuicideRisk.objects.filter(encrypted_file__belongs_to=pk).order_by('-encrypted_file__created_at'),
        'customer':customer,
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section4/components/history_suicide_risk.html',context)


@login_required(login_url='/login')
def section_four_document_behavioral_health_history(request,pk):
    customer=get_object_or_404(Customer, pk=pk)     
    context = {
        'behavioral_health_evaluations': BehavioralHealth.objects.filter(encrypted_file__belongs_to=pk).order_by('-encrypted_file__created_at'),
        'customer':customer,
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section4/components/history_behavioral_health.html',context)


@login_required(login_url='/login')
def section_four_document_bio_psycho_social_history(request,pk):
    customer=get_object_or_404(Customer, pk=pk)     
    context = {
        'bio_psycho_social_assessments': BioPsychoSocial.objects.filter(encrypted_file__belongs_to=pk).order_by('-encrypted_file__created_at'),
        'customer':customer,
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section4/components/history_bio_psycho_social.html',context)


@login_required(login_url='/login')
def section_four_document_brief_behavioral_health_history(request,pk):
    customer=get_object_or_404(Customer, pk=pk)     
    context = {
        'brief_behavioral_health_assessments': BriefBehavioralHealth.objects.filter(encrypted_file__belongs_to=pk).order_by('-encrypted_file__created_at'),
        'customer':customer,
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section4/components/history_brief_behavioral_health.html',context)


@login_required(login_url='/login')
def section_four_document_discharge_summary_history(request,pk):
    customer=get_object_or_404(Customer, pk=pk)     
    context = {
        'discharge_sumaries': DischargeSummary.objects.filter(encrypted_file__belongs_to=pk).order_by('-encrypted_file__created_at'),
        'customer':customer,
        'agency': Agency.objects.first()
        }
    return render(request,'pages/customers/actions/sections/section4/components/history_discharge_sumary.html',context)



# CRUD Generics
def create_focus_area(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    form = FocusAreaForm(request.POST or None)
    context = {}
    if form.is_valid():
        focus_area = form.save(commit=False)
        focus_area.customer = customer
        focus_area.title = form.cleaned_data['title']
        focus_area.description = form.cleaned_data['description']
        focus_area.focus_area_type = form.cleaned_data['focus_area_type']
        focus_area.save()
        # return redirect('section_four_view', pk=pk)
        
        context['tags'] = 'success'
        context['tag_message'] = 'Focus Area created successfully!'
        context['message'] = 'Focus Area created successfully!'
    else:
        context['tags'] = 'error'
        context['tag_message'] = 'Something went wrong!'
        
    focus_areas = FocusArea.objects.prefetch_related('goal_set__objective_set', 'goal_set__intervention_set')
    context['form'] = form
    context['customer'] = customer
    context['focus_areas'] = focus_areas
    context['goal_form'] = GoalForm()
    context['objective_form'] = ObjectiveForm()
    context['intervention_form'] = InterventionForm()
    return render(request, 'pages/forms/section4/partials/modal_form_add_focus_area.html', context)


def edit_focus_area(request, pk):
    instance = get_object_or_404(FocusArea, pk=pk)
    customer = instance.customer
    context = {}
    form = FocusAreaForm(request.POST or None, instance=instance)
    if form.is_valid():
        focus_area = form.save(commit=False)
        focus_area.customer = customer
        focus_area.title = form.cleaned_data['title']
        focus_area.description = form.cleaned_data['description']
        focus_area.focus_area_type = form.cleaned_data['focus_area_type']
        focus_area.save()
        context['tags'] = 'success'
        context['tag_message'] = 'Focus Area modified successfully!'
        context['message'] = 'Focus Area modified successfully!'
    else:
        context['tags'] = 'error'
        context['tag_message'] = 'Something went wrong!'
    
    context['form'] = form
    context['customer'] = customer
    context['fa'] = instance
    
    return render(request, 'pages/forms/section4/partials/modal_form_edit_focus_area.html', context)

def delete_focus_area(request, pk):
    instance = get_object_or_404(FocusArea, pk=pk)
    customer_pk = instance.customer.pk
    context = {}
    if request.method == 'POST':
        instance.delete()
        context['tags'] = 'success'
        context['tag_message'] = 'Focus Area deleted successfully!'
        context['message'] = 'Focus Area deleted successfully!'
    else:
        context['tags'] = 'error'
        context['tag_message'] = 'Something went wrong!'
    
    focus_areas = FocusArea.objects.prefetch_related('goal_set__objective_set', 'goal_set__intervention_set')
    context['focus_areas'] = focus_areas
    context['goal_form'] = GoalForm()
    context['objective_form'] = ObjectiveForm()
    context['intervention_form'] = InterventionForm()
    
    return render(request, 'pages/forms/section4/partials/focus_area.html', context)    


# GOAL
def create_goal(request, focus_area_id):
    focus_area = get_object_or_404(FocusArea, id=focus_area_id)
    form = GoalForm(request.POST or None, initial={'focus_area': focus_area})
    if form.is_valid():
        goal = form.save(commit=False)
        goal.focus_area = focus_area
        goal.title = form.cleaned_data['title']
        form.save()
        return redirect('section_four_view', pk=focus_area.customer.pk)
    return render(request, 'main/form.html', {'form': form, 'title': 'Crear Goal'})

def edit_goal(request, pk):
    instance = get_object_or_404(Goal, pk=pk)
    focus_area = instance.focus_area
    customer = focus_area.customer
    context = {}
    
    form = GoalForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        context['tags'] = 'success'
        context['tag_message'] = 'Goal modified successfully!'
        context['message'] = 'Goal modified successfully!'
    else:
        context['tags'] = 'error'
        context['tag_message'] = 'Something went wrong!'
    
    context['form'] = form
    context['customer'] = customer
    context['goal'] = instance
    
    return render(request, 'pages/forms/section4/partials/modal_form_edit_goal.html', context)

def delete_goal(request, pk):
    instance = get_object_or_404(Goal, pk=pk)
    focus_area = instance.focus_area
    customer = focus_area.customer
    context = {}
    if request.method == 'POST':
        instance.delete()
        context['tags'] = 'success'
        context['tag_message'] = 'Goal deleted successfully!'
        context['message'] = 'Goal Area deleted successfully!'
    else:
        context['tags'] = 'error'
        context['tag_message'] = 'Something went wrong!'
    
    focus_areas = FocusArea.objects.prefetch_related('goal_set__objective_set', 'goal_set__intervention_set')
    context['customer'] = customer
    context['focus_areas'] = focus_areas
    context['goal_form'] = GoalForm()
    context['objective_form'] = ObjectiveForm()
    context['intervention_form'] = InterventionForm()
    
    return render(request, 'pages/forms/section4/partials/focus_area.html', context)


# OBJECTIVE
def create_objective(request, goal_id):
    goal = get_object_or_404(Goal, id=goal_id)
    form = ObjectiveForm(request.POST or None, initial={'goal': goal})
    if form.is_valid():
        form.save()
        return redirect('hierarchy')
    return render(request, 'main/form.html', {'form': form, 'title': 'Crear Objetivo'})

def edit_objective(request, pk):
    instance = get_object_or_404(Objective, pk=pk)
    goal = instance.goal
    focus_area = goal.focus_area
    customer = focus_area.customer
    form = ObjectiveForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('section_four_view', pk=customer.pk)
    return render(request, 'main/form.html', {'form': form, 'title': 'Editar Objetivo'})

def delete_objective(request, pk):
    instance = get_object_or_404(Objective, pk=pk)
    goal = instance.goal
    focus_area = goal.focus_area
    customer = focus_area.customer
    if request.method == 'POST':
        instance.delete()
        return redirect('section_four_view', pk=customer.pk)
    return render(request, 'main/confirm_delete.html', {'object': instance})


# INTERVENTION
def create_intervention(request, objective_id):
    objetivo = get_object_or_404(Objective, id=objective_id)
    form = InterventionForm(request.POST or None, initial={'objetivo': objetivo})
    if form.is_valid():
        form.save()
        return redirect('hierarchy')
    return render(request, 'main/form.html', {'form': form, 'title': 'Crear Intervención'})

def edit_intervention(request, pk):
    instance = get_object_or_404(Intervention, pk=pk)
    goal = instance.goal
    focus_area = goal.focus_area
    customer = focus_area.customer
    form = InterventionForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('section_four_view', pk=customer.pk)
    return render(request, 'main/form.html', {'form': form, 'title': 'Editar Intervención'})

def delete_intervention(request, pk):
    instance = get_object_or_404(Intervention, pk=pk)
    goal = instance.goal
    focus_area = goal.focus_area
    customer = focus_area.customer
    if request.method == 'POST':
        instance.delete()
        return redirect('section_four_view', pk=customer.pk)
    return render(request, 'main/confirm_delete.html', {'object': instance})


@require_POST
def create_goal_inline(request, focus_area_id):
    focus_area = get_object_or_404(FocusArea, pk=focus_area_id)
    customer = focus_area.customer
    context = {}
    form = GoalForm(request.POST)
    if form.is_valid():
        goal = form.save(commit=False) 
        goal.focus_area = focus_area 
        goal.save()
        context['tags'] = 'success'
        context['tag_message'] = 'Goal created successfully!'
        context['message'] = 'Goal created successfully!'
    else:
        context['tags'] = 'error'
        context['tag_message'] = 'Something went wrong!'
    
    focus_areas = FocusArea.objects.prefetch_related('goal_set__objective_set', 'goal_set__intervention_set')
    context['form'] = form
    context['customer'] = customer
    context['fa'] = focus_area
    
    return render(request, 'pages/forms/section4/partials/goal_creation_form.html', context)
    
    

@require_POST
def create_objective_inline(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    focus_area = goal.focus_area
    customer = focus_area.customer
    form = ObjectiveForm(request.POST)
    if form.is_valid():
        objective = form.save(commit=False)  
        objective.goal = goal
        objective.save()  
    return redirect('section_four_view', pk=customer.pk)

@require_POST
def create_intervention_inline(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    focus_area = goal.focus_area
    customer = focus_area.customer
    form = InterventionForm(request.POST)
    if form.is_valid():
        intervention = form.save(commit=False)
        intervention.goal = goal
        intervention.description = form.cleaned_data['description']
        intervention.save()
    return redirect('section_four_view', pk=customer.pk)