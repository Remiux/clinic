from django.core.paginator import Paginator

def _get_paginator(request, object_list):
    object_list = object_list.order_by('id')  # Ordenar la lista de objetos
    paginator = Paginator(object_list, 6)  # 6 objetos por página
    page_number = request.GET.get('page', 1)
    page_object = paginator.get_page(page_number)
    
    context = {
        'paginator': page_object
    }
    
    return context