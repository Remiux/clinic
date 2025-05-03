from apps.symptom.models import IndividualTherapy,IndividualTherapySection
from django.utils import timezone
from datetime import timedelta

def validate_creation(individual_therapy):
        # return True
        today = timezone.now().date().today()
        print(today)
        # Calcular el inicio de la semana (lunes)
        start_of_week = today - timedelta(days=today.weekday())
        # Calcular el final de la semana (domingo)
        end_of_week = start_of_week + timedelta(days=6)
        print(start_of_week)
        print(end_of_week)
        # Verificar si existe alguna terapia para este cliente en la semana actual
        exists = IndividualTherapySection.objects.filter(
            individual_therapy_pk=individual_therapy.pk,
            create_at__gte=start_of_week,
            create_at__lte=end_of_week,
        ).exists()
        return exists