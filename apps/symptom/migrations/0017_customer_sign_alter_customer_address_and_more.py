# Generated by Django 5.1.7 on 2025-04-10 05:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('symptom', '0016_alter_encryptedfile_belongs_to'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='sign',
            field=models.ImageField(blank=True, null=True, upload_to='customer_sign'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='customer',
            name='case_no',
            field=models.CharField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='city',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='contact_no',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='diagnostic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='symptom.diagnostic'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='dob',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='emergency_contact_person',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='customer',
            name='emergency_contact_phone_number',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='emergency_contact_relationship',
            field=models.CharField(max_length=80),
        ),
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='customer',
            name='insurance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='symptom.insurance'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='last_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='customer',
            name='medicaid_no',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='movile',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='customer',
            name='ssn',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='state',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='customer',
            name='zip',
            field=models.CharField(max_length=50),
        ),
    ]
