from django.core.paginator import Paginator

def _get_paginator(request, object_list):
    paginator = Paginator(object_list, 50)  # 6 objetos por página
    page_number = request.GET.get('page', 1)
    page_object = paginator.get_page(page_number)
    
    context = {
        'paginator': page_object
    }
    
    return context