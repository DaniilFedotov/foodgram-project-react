from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название тега')
    color = models.CharField(
        max_length=7,
        unique=True,
        verbose_name='Цвет тега')
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='Раздел тега')

    def __str__(self):
        return self.name


class Recipe(models.Model):
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги',
        through='RecipeTag')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта')
    ingredients = models.ManyToManyField(
        'Ingredient',
        related_name='recipes',
        verbose_name='Ингредиенты',
        through='RecipeIngredient')
    is_favorited = models.BooleanField(
        null=True,  # Временно
        verbose_name='Находится ли в избранном')
    is_in_shopping_cart = models.BooleanField(
        null=True,  # Временно
        verbose_name='Находится ли в корзине')
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта')
    #image = models.ImageField()
    text = models.TextField(
        verbose_name='Описание рецепта')
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления (в минутах)')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True)
    measurement_unit = models.CharField(
        max_length=200)

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE)
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE)


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(
        verbose_name='Количество')
