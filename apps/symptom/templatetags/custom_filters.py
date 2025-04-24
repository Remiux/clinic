import os
from django import template

register = template.Library()

@register.filter
def basename(value):
    """Devuelve solo el nombre del archivo con su extensión."""
    return os.path.basename(value)

@register.filter
def exclude_elegibility_files(files):
    """
    Excluye archivos cuyo nombre contenga 'elegibility_' (insensible a mayúsculas).
    """
    return [file for file in files if not os.path.basename(file.file.name).lower().startswith('elegibility_')]