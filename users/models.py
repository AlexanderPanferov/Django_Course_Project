from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=150, unique=True, verbose_name='Почта')
    verified = models.BooleanField(default=False, verbose_name='подтвержден')
    verification_code = models.IntegerField(verbose_name='ключ подтверждения', **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
