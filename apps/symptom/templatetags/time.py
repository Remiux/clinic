from django import template

register = template.Library()

@register.filter
def format_time(value):
    """Convierte '8:00' a '08:00' para HTML5."""
    if ':' in value:
        hours, minutes = value.split(':')
        return f"{int(hours):02d}:{minutes}"
    return value