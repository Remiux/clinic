from django.shortcuts import render,get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from apps.accounts.models import MasterGenerate
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
    # Verificar si el cliente está en una terapia individual
    is_in_individual_therapy = IndividualTherapySection.objects.filter(customer=customer).exists()
    master = Master.objects.filter(user=request.user,customer = customer).first()
    # Verificar si el cliente está en un terapia PSR
    is_in_group_customer = CustomerPSRSections.objects.filter(customer=customer).exists()
    focus_areas = FocusArea.objects.prefetch_related('goal__objective_set').order_by('-focus_area_type')
    is_in_individual_therapy = IndividualTherapy.objects.filter(customer=customer).exists()

    # Verificar si el cliente está en un terapia PSR
    is_in_group_customer = GroupCustomer.objects.filter(customer=customer).exists()
    
    focus_areas = FocusArea.objects.prefetch_related('goal__objective_set').order_by('-focus_area_type')
    context = {
        'master':master,
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
    focus_areas = FocusArea.objects.prefetch_related('goal__objective_set').order_by('-focus_area_type')
    
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
    master = get_object_or_404(Master, pk=pk)
    form = FocusAreaForm(request.POST or None)
    context = {}
    if form.is_valid():
        
        focus_area = form.save(commit=False)
        focus_area.number = FocusArea.objects.filter(master=master).count()+1
        focus_area.master = master
        focus_area.save()
        # return redirect('section_four_view', pk=pk)
        
        context['tags'] = 'success'
        context['tag_message'] = 'Focus Area created successfully!'
        context['message'] = 'Focus Area created successfully!'
    else:
        context['tags'] = 'error'
        context['tag_message'] = 'Something went wrong!'
        
    focus_areas = FocusArea.objects.prefetch_related('goal__objective_set')
    context['form'] = form
    context['master']= master
    context['customer'] = master.customer
    context['focus_areas'] = focus_areas
    context['goal_form'] = GoalForm()
    context['objective_form'] = ObjectiveForm()
    context['intervention_form'] = InterventionForm()
    return render(request, 'pages/forms/section4/partials/modal_form_add_focus_area.html', context)


def edit_focus_area(request, pk):
    instance = get_object_or_404(FocusArea, pk=pk)
    master = instance.master
    context = {}
    form = FocusAreaForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        context['tags'] = 'success'
        context['tag_message'] = 'Focus Area modified successfully!'
        context['message'] = 'Focus Area modified successfully!'
    else:
        context['tags'] = 'error'
        context['tag_message'] = 'Something went wrong!'
    
    context['form'] = form
    context['master'] = master
    context['customer'] = master.customer
    context['focus_area'] = instance
    
    return render(request, 'pages/forms/section4/partials/modal_form_edit_focus_area.html', context)

def delete_focus_area(request, pk):
    instance = get_object_or_404(FocusArea, pk=pk)
    master = instance.master
    context = {}
    if request.method == 'POST':
        instance.delete()
        context['tags'] = 'success'
        context['tag_message'] = 'Focus Area deleted successfully!'
        context['message'] = 'Focus Area deleted successfully!'
        index=1
        for focus_area in FocusArea.objects.filter(master=instance.master).order_by('id'):
            focus_area.number = index
            index=index+1
            focus_area.save()
    else:
        context['tags'] = 'error'
        context['tag_message'] = 'Something went wrong!'
    
    focus_areas = FocusArea.objects.prefetch_related('goal__objective_set')
    context['focus_areas'] = focus_areas
    context['goal_form'] = GoalForm()
    context['objective_form'] = ObjectiveForm()
    context['intervention_form'] = InterventionForm()
    context['fa'] = instance
    context['master'] = master
    context['customer'] = master.customer
    
    return render(request, 'pages/forms/section4/partials/focus_area.html', context)    


# GOAL
def create_goal(request, focus_area_id):
    focus_area = get_object_or_404(FocusArea, id=focus_area_id)
    form = GoalForm(request.POST or None, initial={'focus_area': focus_area})
    if form.is_valid():
        goal = form.save(commit=False)
        goal.focus_area = focus_area
        form.save()
        return redirect('section_four_view', pk=focus_area.master.customer.pk)
    return render(request, 'main/form.html', {'form': form, 'title': 'Crear Goal'})

def edit_goal(request, pk):
    instance = get_object_or_404(Goal, pk=pk)
    focus_area = instance.focus_area
    customer = focus_area.master.customer
    context = {
        'focus_area':focus_area
    }
    
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
    context['master'] = focus_area.master
    context['goal'] = instance
    
    return render(request, 'pages/forms/section4/partials/modal_form_edit_goal.html', context)

def delete_goal(request, pk):
    instance = get_object_or_404(Goal, pk=pk)
    focus_area = instance.focus_area
    customer = focus_area.master.customer
    context = {}
    if request.method == 'POST':
        instance.delete()
        context['tags'] = 'success'
        context['tag_message'] = 'Goal deleted successfully!'
        context['message'] = 'Goal Area deleted successfully!'
        
    else:
        context['tags'] = 'error'
        context['tag_message'] = 'Something went wrong!'
    
    focus_areas = FocusArea.objects.prefetch_related('goal__objective_set')
    context['customer'] = customer
    context['master']=focus_area.master
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
    customer = focus_area.master.customer
    context = {}
    form = ObjectiveForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        context['tags'] = 'success'
        context['tag_message'] = 'Objective modified successfully!'
        context['message'] = 'Objective modified successfully!'
    else:
        context['tags'] = 'error'
        context['tag_message'] = 'Something went wrong!'
    context['focus_area'] = focus_area
    context['form'] = form
    context['customer'] = customer
    context['master'] = focus_area.master
    context['obj'] = instance
    
    return render(request, 'pages/forms/section4/partials/modal_form_edit_objective.html', context)

def delete_objective(request, pk):
    instance = get_object_or_404(Objective, pk=pk)
    goal = instance.goal
    focus_area = goal.focus_area
    customer = focus_area.master.customer
    context = {}
    if request.method == 'POST':
        instance.delete()
        context['tags'] = 'success'
        context['tag_message'] = 'Objective deleted successfully!'
        context['message'] = 'Objective deleted successfully!'
        index=1
        for objetive in Objective.objects.filter(goal=goal).order_by('id'):
            objetive.number = index
            index=index+1
            objetive.save()
    else:
        context['tags'] = 'error'
        context['tag_message'] = 'Something went wrong!'
    
    focus_areas = FocusArea.objects.prefetch_related('goal__objective_set')
    context['customer'] = customer
    context['master'] = focus_area.master
    context['focus_areas'] = focus_areas
    context['goal_form'] = GoalForm()
    context['objective_form'] = ObjectiveForm()
    context['intervention_form'] = InterventionForm()
    
    return render(request, 'pages/forms/section4/partials/focus_area.html', context)


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
    context = {}
    form = InterventionForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        context['tags'] = 'success'
        context['tag_message'] = 'Intervention modified successfully!'
        context['message'] = 'Intervention modified successfully!'
    else:
        context['tags'] = 'error'
        context['tag_message'] = 'Something went wrong!'
    
    context['form'] = form
    context['customer'] = customer
    context['interv'] = instance
    
    return render(request, 'pages/forms/section4/partials/modal_form_edit_intervention.html', context)

def delete_intervention(request, pk):
    instance = get_object_or_404(Intervention, pk=pk)
    goal = instance.goal
    focus_area = goal.focus_area
    customer = focus_area.customer
    context = {}
    if request.method == 'POST':
        instance.delete()
        context['tags'] = 'success'
        context['tag_message'] = 'Intervention deleted successfully!'
        context['message'] = 'Intervention deleted successfully!'
    else:
        context['tags'] = 'error'
        context['tag_message'] = 'Something went wrong!'
    
    focus_areas = FocusArea.objects.prefetch_related('goal__objective_set')
    context['customer'] = customer
    context['focus_areas'] = focus_areas
    context['goal_form'] = GoalForm()
    context['objective_form'] = ObjectiveForm()
    context['intervention_form'] = InterventionForm()
    
    return render(request, 'pages/forms/section4/partials/focus_area.html', context)



@require_POST
def create_goal_inline(request, focus_area_id):
    focus_area = get_object_or_404(FocusArea, pk=focus_area_id)
    master = focus_area.master
    context = {}
    form = GoalForm()
    if not Goal.objects.filter(focus_area = focus_area):
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
    else:
        context['tags'] = 'error'
        context['tag_message'] = 'You have one goal for this focus area!'
    context['form'] = form
    context['master'] = master
    context['customer'] = master.customer
    context['focus_area'] = focus_area
    
    return render(request, 'pages/forms/section4/partials/goal_creation_form.html', context)
    
    

@require_POST
def create_objective_inline(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    focus_area = goal.focus_area
    customer = focus_area.master.customer
    context = {}
    form = ObjectiveForm(request.POST)
    if form.is_valid():
        objective = form.save(commit=False)  
        objective.number = Objective.objects.filter(goal=goal).count() + 1
        objective.goal = goal
        objective.save() 
        context['tags'] = 'success'
        context['tag_message'] = 'Objective created successfully!'
        context['message'] = 'Objective created successfully!'
    else:
        context['tags'] = 'error'
        context['tag_message'] = 'Something went wrong!'
    
    context['focus_area'] = focus_area
    context['form'] = form
    context['customer'] = customer
    context['master'] = focus_area.master
    context['goal'] = goal
    
    return render(request, 'pages/forms/section4/partials/objective_creation_form.html', context)

@require_POST
def create_intervention_inline(request, goal_id):
    goal = get_object_or_404(Goal, pk=goal_id)
    focus_area = goal.focus_area
    customer = focus_area.customer
    form = InterventionForm(request.POST)
    context = {}
    if form.is_valid():
        intervention = form.save(commit=False)
        intervention.goal = goal
        intervention.description = form.cleaned_data['description']
        intervention.save()
        context['tags'] = 'success'
        context['tag_message'] = 'Intervention created successfully!'
        context['message'] = 'Intervention created successfully!'
    else:
        context['tags'] = 'error'
        context['tag_message'] = 'Something went wrong!'
    
    context['form'] = form
    context['customer'] = customer
    context['goal'] = goal
    
    return render(request, 'pages/forms/section4/partials/intervention_creation_form.html', context)


def update_treatment_duration(request, pk):
    master = get_object_or_404(Master, pk=pk)
    customer = master.customer
    context = {}
    if request.method == 'POST':
        duration = request.POST.get('treatment_duration')
        duration_other = request.POST.get('treatment_duration_other')

        if duration == '3':
            master.treatment_duration = 3
        elif duration == '6':
            master.treatment_duration = 6
        elif duration_other and duration_other.strip().isdigit():
            duration_value = int(duration_other.strip())
            if 1 <= duration_value <= 6:
                master.treatment_duration = duration_value
            else:
                # Si el valor está fuera del rango permitido, devolver un mensaje de error
                context['tags'] = 'error'
                context['master']=master
                context['tag_message'] = 'Please select a treatment duration between 1 and 6.'
                context['message'] = 'Please select a treatment duration between 1 and 6.'
                context['customer'] = customer
                return render(request, 'pages/forms/section4/partials/treatment_duration_form.html', context)
        else:
            # Si no hay un valor válido, devolver un mensaje de error
            context['tags'] = 'error'
            context['master']=master
            context['tag_message'] = 'Please select a valid treatment duration.'
            context['message'] = 'Please select a valid treatment duration.'
            context['customer'] = customer
            return render(request, 'pages/forms/section4/partials/treatment_duration_form.html', context)

        customer.save()
        context['tags'] = 'success'
        context['master']=master
        context['tag_message'] = 'Treatment duration updated successfully!'
        context['message'] = 'Treatment duration updated successfully!'
        context['customer'] = customer
    
    return render(request, 'pages/forms/section4/partials/treatment_duration_form.html', context)

@login_required(login_url='/login')
def update_psr_master_view(request, pk):
    master = get_object_or_404(Master,pk=pk)
    if master.as_psr:
            master.as_psr = False
    else: 
            master.as_psr = True
    master.save()
    context={
        'master':master,
        'customer':master.customer
    }
    return render(request, 'pages/forms/section4/master_document.html',context)

@login_required(login_url='/login')
def update_individual_therapy_master_view(request, pk):
    master = get_object_or_404(Master,pk=pk)
    if master.as_individual_therapy:
        master.as_individual_therapy = False
    else: 
        master.as_individual_therapy = True
    master.save()
    context={
        'master':master,
        'customer':master.customer
    }
    return render(request, 'pages/forms/section4/master_document.html',context)

@login_required(login_url='/login')
def update_initial_discharge_criteria_master_view(request, pk):
    master = get_object_or_404(Master,pk=pk)
    form = MasterInitialDischargeCriteriaForm(instance = master)
    message=""
    if request.POST:
        form = MasterInitialDischargeCriteriaForm(request.POST,instance = master)
        if form.is_valid():
            form.save()
            message = "Change Successfull"
    context={
        'master':master,
        'form':form,
        'message':message
    }
    return render(request, 'pages/forms/section4/partials/initial_discharge_criteria.html',context)


@login_required(login_url='/login')
def confirm_master_view(request, pk):
    master =  get_object_or_404(Master,pk=pk)
    master.is_active = False
    master.save()
    context = {
        'master':master,
        'focus_areas' : FocusArea.objects.prefetch_related('goal__objective_set').order_by('-focus_area_type')
    }
    return render(request,'pages/forms/section4/master_document.html',context)