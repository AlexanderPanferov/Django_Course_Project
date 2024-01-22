from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=150, unique=True, verbose_name='Почта')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
