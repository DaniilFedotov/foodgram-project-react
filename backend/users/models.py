"""
from django.db import models
from django.contrib.auth.models import AbstractUser

from .user_roles import UserRoles


class User(AbstractUser):
    email = models.EmailField(
        max_length=256,
        unique=True,)
    username = models.CharField(
        max_length=150,
        unique=True)
    first_name = models.CharField(
        max_length=150,
        unique=True)
    last_name = models.CharField(
        max_length=150,
        unique=True)
    role = models.CharField(
    max_length=150,
    verbose_name='Роль',
    choices=UserRoles.choices,
    default=UserRoles.NOT_AUTH_USER,)

    def __str__(self):
        return f'{self.username}'

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_auth_user(self):
        return self.role == UserRoles.AUTH_USER

    @property
    def is_not_auth_user(self):
        return self.role == UserRoles.NOT_AUTH_USER
"""