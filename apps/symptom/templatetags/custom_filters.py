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
    Excluye archivos cuyo nombre contenga 'elegibility' (insensible a mayúsculas).
    """
    return [file for file in files if not os.path.basename(file.file.name).lower().startswith('elegibility')]

@register.filter
def exclude_psychiatric_evaluation_files(files):
    """
    Excluye archivos cuyo nombre contenga 'psychiatric_evaluation' (insensible a mayúsculas).
    """
    return [file for file in files if not os.path.basename(file.file.name).lower().startswith('psychiatric_evaluation')]

@register.filter
def exclude_yearly_physical_files(files):
    """
    Excluye archivos cuyo nombre contenga 'yearly_physical' (insensible a mayúsculas).
    """
    return [file for file in files if not os.path.basename(file.file.name).lower().startswith('yearly_physical')]

@register.filter
def exclude_suicide_risk_assessment_files(files):
    """
    Excluye archivos cuyo nombre contenga 'suicide_risk_assessment_' (insensible a mayúsculas).
    """
    return [file for file in files if not os.path.basename(file.file.name).lower().startswith('suicide_risk_assessment')]

@register.filter
def exclude_behavioral_health_evaluation_files(files):
    """
    Excluye archivos cuyo nombre contenga 'behavioral_health_evaluation_' (insensible a mayúsculas).
    """
    return [file for file in files if not os.path.basename(file.file.name).lower().startswith('behavioral_health_evaluation')]

@register.filter
def exclude_bio_psycho_social_assessment_files(files):
    """
    Excluye archivos cuyo nombre contenga 'bio_psycho_social_assessment_' (insensible a mayúsculas).
    """
    return [file for file in files if not os.path.basename(file.file.name).lower().startswith('bio_psycho_social_assessment')]

@register.filter
def exclude_brief_behavioral_health_assessment_files(files):
    """
    Excluye archivos cuyo nombre contenga 'brief_behavioral_health_assessment_' (insensible a mayúsculas).
    """
    return [file for file in files if not os.path.basename(file.file.name).lower().startswith('brief_behavioral_health_assessment')]

@register.filter
def exclude_discharge_summary_files(files):
    """
    Excluye archivos cuyo nombre contenga 'discharge_summary_' (insensible a mayúsculas).
    """
    return [file for file in files if not os.path.basename(file.file.name).lower().startswith('discharge_summary')]