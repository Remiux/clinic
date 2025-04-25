from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from apps.symptom.models import  Customer, CustomerPSRSections, GroupsPSRSections, TherapistsGroups



# Create your views here.


@login_required(login_url='/login')
def therapists_customer_check_view(request,pk):
    group = get_object_or_404(TherapistsGroups, pk=pk)
    customers = Customer.objects.exclude(
    id__in=group.group_customer.all().values('customer_id')
    ).order_by('first_name')
    context = {
        'group':group,
        'customers':customers
    }
    section = GroupsPSRSections.objects.filter(group_pk=group.pk,is_active=True).first()
    if request.method == 'POST':
        if not section: 
            section=GroupsPSRSections.objects.create(
                    group_pk=group.pk,
                    therapist_pk=group.therapist.pk,
                    therapist_full_name= f"{group.therapist.first_name} {group.therapist.last_name}",
                )
            for customer in group.group_customer.all():
                    CustomerPSRSections.objects.create(
                        section=section,
                        customer=customer.customer, 
                    )
                    
    context['section']= section
    return render(request,'pages/therapistsGroup/actions/sections/index.html',context)


@login_required(login_url='/login')
def therapists_customer_checked_assist_view(request,pk):
    customer = get_object_or_404(CustomerPSRSections, pk=pk)
    if request.method == 'POST':
        if customer.assist:
            customer.assist = False
        else:
            customer.assist = True  
        customer.save()
    context = {
        'customer':customer,
    }
    return render(request,'pages/therapistsGroup/actions/sections/sectionCustomerCard.html',context)


@login_required(login_url='/login')
def therapists_customer_checked_all_assist_view(request,pk):
    section = get_object_or_404(GroupsPSRSections, pk=pk)
    if request.method == 'POST':
        for customer in section.customer_psr_section.all():
            customer.assist = True
            customer.save()
    context = {
        'section':section,
    }
    return render(request,'pages/therapistsGroup/actions/sections/sectionCustomerList.html',context)


@login_required(login_url='/login')
def therapists_customer_unchecked_all_assist_view(request,pk):
    section = get_object_or_404(GroupsPSRSections, pk=pk)
    if request.method == 'POST':
        for customer in section.customer_psr_section.all():
            customer.assist = False
            customer.save()
    context = {
        'section':section,
    }
    return render(request,'pages/therapistsGroup/actions/sections/sectionCustomerList.html',context)


@login_required(login_url='/login')
def therapists_add_customer_assist_view(request,pk):
    section = get_object_or_404(GroupsPSRSections, pk=pk)
    context = {}
    if request.method == 'POST':
        customer = Customer.objects.get(pk=request.POST['customer'])
        if section.customer_psr_section.filter(customer=customer).exists():
            context['error_messsage']="The customer is listed"
            context['tags']="error"
        else:
            CustomerPSRSections.objects.create(
                    section=section,
                    customer=customer, 
                )
    context['section']=section
    return render(request,'pages/therapistsGroup/actions/sections/sectionCustomerList.html',context)

@login_required(login_url='/login')
def therapists_customer_remove_assist_list_view(request,pk):
    customer = get_object_or_404(CustomerPSRSections, pk=pk)
    context = {
        'customer':customer,
    }
    if request.method == 'DELETE':
        customer.delete()
        context['customer']=[]
    
    return render(request,'pages/therapistsGroup/actions/sections/sectionCustomerCard.html',context)


@login_required(login_url='/login')
def therapists_confirm_assist_view(request,pk):
    section = get_object_or_404(GroupsPSRSections, pk=pk)
    group = get_object_or_404(TherapistsGroups,pk=int(section.group_pk))
    if request.method == 'POST':
        section.init_hour = request.POST['init_hour']
        section.end_hour = request.POST['end_hour']
        section.is_active = False
        section.save()
        new_section=GroupsPSRSections.objects.create(
                    group_pk=group.pk,
                    therapist_pk=group.therapist.pk,
                    therapist_full_name= f"{group.therapist.first_name} {group.therapist.last_name}",
                )
        for customer in group.group_customer.all():
                    CustomerPSRSections.objects.create(
                        section=new_section,
                        customer=customer.customer, 
                    )
    return redirect('therapists_customer_check_view', pk=group.pk)