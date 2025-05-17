from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
# Create your models here.


class User(AbstractUser):
    phone_number = models.PositiveIntegerField(blank=True, null=True)
    sign= models.ImageField(upload_to='user_sign',blank=True,null=True)
    is_master= models.BooleanField(default=False)
    
    
class MasterGenerate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='master_generate_user')
    create_at = models.DateTimeField(auto_created=True,default=timezone.now)
    generate_date = models.DateField()
    generate_init_time = models.TimeField()
    generate_end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    customer_pk = models.CharField(max_length=20)
    customer_full_name = models.CharField(max_length=80)
    