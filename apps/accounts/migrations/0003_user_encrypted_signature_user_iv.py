# Generated by Django 5.1.7 on 2025-04-02 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_user_sign'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='encrypted_signature',
            field=models.BinaryField(null=True)
        ),
        migrations.AddField(
            model_name='user',
            name='iv',
            field=models.BinaryField(null=True)
        ),
    ]
