from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(
        max_length=256,
        unique=True,
        verbose_name='Электронная почта')
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Логин пользователя')
    first_name = models.CharField(
        null=True,  # Временно
        max_length=150,
        verbose_name='Имя пользователя')
    last_name = models.CharField(
        null=True,  # Временно
        max_length=150,
        verbose_name='Фамилия пользователя')
    password = models.CharField(
        max_length=150,
        verbose_name='Пароль пользователя')

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username
