from django.db import models


class UserRoles(models.TextChoices):
    ADMIN = 'admin'
    AUTH_USER = 'auth_user'
    NOT_AUTH_USER = 'not_auth_user'