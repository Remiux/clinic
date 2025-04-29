from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from apps.accounts.models import User
from apps.symptom.filters import TherapistsGroupsFilter
from apps.symptom.form import GroupCustomerForm, TherapistsGroupsForm
from apps.symptom.models import Customer, GroupCustomer, TherapistsGroups
from utils.paginator import _get_paginator


# Create your views here.
@login_required(login_url='/login')
def individual_terapy_view(request):
    context = _show_individual_terapy_filter(request)
    context['therapists'] = User.objects.filter(groups__name='therapist').order_by('first_name')
    return render(request,'pages/indivualTherapy/index.html',context)


@login_required(login_url='/login')
def filter_individual_terapy_view(request):
    context=_show_individual_terapy_filter(request)
    return render(request,'pages/indivualTherapy/GroupsCardList.html',context)

def _show_individual_terapy_filter(request):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    customers = TherapistsGroupsFilter(request.GET, queryset=TherapistsGroups.objects.all().order_by('-pk'))
    context = _get_paginator(request, customers.qs)
    context['parameters'] = parameters
    return context



