from django.db import models
from ..users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=256,  # ?
        verbose_name='Название тега')
    color = models.CharField()  # Точно?
    slug = models.SlugField(
        max_length=50,  # ?
        unique=True,
        verbose_name='Раздел тега')

    def __str__(self):
        return f'{self.name}'


class Recipe(models.Model):
    tags = models.ForeignKey(
        Tag,
        related_name='recipes',)
    author = models.ForeignKey(
        User,
        related_name='recipes',)
    ingredients = models.ManyToManyField(
        'Ingredient',
        through='RecipeIngredient',)
    name = models.CharField(
        max_length=200,  # Задано явно
        verbose_name='Название рецепта',)
    image = models.ImageField()
    text = models.TextField(
        max_length=1500,
        verbose_name='Описание рецепта',)
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)')  # ДБ больше 1


    def __str__(self):
        return f'{self.name}'


class ShoppingCart(models.Model):
    content = models.ForeignKey(
        Recipe,
        many=True,
        verbose_name='Список покупок'
    )


class Ingredient(models.Model):
    name = 'jh,j'

    def __str__(self):
        return f'{self.name}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,  # on_delete
    )
    ingredient = models.ForeignKey(
        Ingredient,  # on_delete
    )
