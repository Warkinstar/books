from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Можем дополнить различными полями"""
    middle_name = models.CharField(("Отчество"), max_length=150, blank=True)
