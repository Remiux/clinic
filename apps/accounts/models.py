from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
# Create your models here.


class User(AbstractUser):
    phone_number = models.PositiveIntegerField(blank=True, null=True)
    sign= models.ImageField(upload_to='user_sign',blank=True,null=True)
    