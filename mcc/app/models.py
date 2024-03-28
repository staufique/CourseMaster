from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from datetime import datetime
from .manager import CustomBaseUserManager

class User(AbstractUser):
    username=None
    name=models.CharField(max_length=250,null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=14)
    dob = models.DateField(null=True)
    city = models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomBaseUserManager()

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]