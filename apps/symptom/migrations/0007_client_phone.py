# Generated by Django 5.1.7 on 2025-04-09 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('symptom', '0006_diagnostic'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='phone',
            field=models.IntegerField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
