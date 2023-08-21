from django.db import models

from home.models import BaseModel
from home.utils import RolesEnum
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=10, choices=RolesEnum.choices())


class Client(BaseModel):
    advisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advisors')
