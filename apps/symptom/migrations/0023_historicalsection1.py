# Generated by Django 5.1.7 on 2025-04-15 17:07

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('symptom', '0022_rename_addresss_agency_address'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalSection1',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_datetime_at', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('create_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_section1', to=settings.AUTH_USER_MODEL)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historical_section1', to='symptom.customer')),
            ],
            options={
                'verbose_name': 'HistoricalSection1',
                'verbose_name_plural': 'HistoricalSection1s',
            },
        ),
    ]
