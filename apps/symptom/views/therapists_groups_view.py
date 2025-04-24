from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from apps.symptom.filters import TherapistsGroupsFilter
from apps.symptom.models import TherapistsGroups
from utils.paginator import _get_paginator


# Create your views here.
@login_required(login_url='/login')
def therapists_groups_view(request):
    context = _show_therapists_groups_filter(request)

    return render(request,'pages/therapistsGroup/index.html',context)


@login_required(login_url='/login')
def filter_therapists_groups_view(request):
    context=_show_therapists_groups_filter(request)
    return render(request,'pages/therapistsGroup/GroupsCardList.html',context)

def _show_therapists_groups_filter(request):
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    customers = TherapistsGroupsFilter(request.GET, queryset=TherapistsGroups.objects.all().order_by('pk'))
    context = _get_paginator(request, customers.qs)
    context['parameters'] = parameters
    return context



@login_required(login_url='/login')
def detail_therapists_groups_view(request, pk):
    context = {'group':get_object_or_404(TherapistsGroups, pk=pk)} 
    return render(request, 'pages/therapistsGroup/actions/detail/GroupDetail.html', context)