from django.db import models
#from django.contrib.auth.models import AbstractUser

from users.models import User

"""
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

    def __str__(self):
        return f'{self.username}'
"""

class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        null=True,
        verbose_name='Название тега')
    color = models.CharField(
        max_length=7,
        null=True,
        verbose_name='Цвет тега')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Раздел тега')

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    tags = models.ForeignKey(
        Tag,
        null=True,
        on_delete=models.SET_NULL,
        related_name='recipes')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes')
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient')
    is_favorited = models.BooleanField(
        verbose_name='Находится ли в избранном')
    is_in_shopping_cart = models.BooleanField(
        verbose_name='Находится ли в корзине')
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта')
    image = models.BinaryField()  #
    text = models.TextField(
        verbose_name='Описание рецепта')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)')


    def __str__(self):
        return f'{self.name}'


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True)
    measurement_unit = models.CharField(
        max_length=200)

    def __str__(self):
        return f'{self.name}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE)
