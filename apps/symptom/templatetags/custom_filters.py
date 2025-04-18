import os
from django import template

register = template.Library()

@register.filter
def basename(value):
    """Devuelve solo el nombre del archivo con su extensión."""
    return os.path.basename(value)