from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        max_length=256,
        unique=True,)
    username = models.CharField(
        max_length=150,
        unique=True)
    first_name = models.CharField(
        null=True,  # Временно
        max_length=150,
        unique=True)
    last_name = models.CharField(
        null=True,  # Временно
        max_length=150,
        unique=True)
    password = models.CharField(
        max_length=150)
    #role = models.CharField(max_length=100)

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username
