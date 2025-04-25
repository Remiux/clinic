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
    return [file for file in files if not os.path.basename(file.file.name).lower().startswith('elegibility')]

@register.filter
def exclude_psychiatric_evaluation_files(files):
    """
    Excluye archivos cuyo nombre contenga 'psychiatric_evaluation_' (insensible a mayúsculas).
    """
    return [file for file in files if not os.path.basename(file.file.name).lower().startswith('psychiatric_evaluation')]

@register.filter
def exclude_yearly_physical_files(files):
    """
    Excluye archivos cuyo nombre contenga 'yearly_physical' (insensible a mayúsculas).
    """
    return [file for file in files if not os.path.basename(file.file.name).lower().startswith('yearly_physical')]