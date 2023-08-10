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


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик')
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'], name='follow_unique')]
