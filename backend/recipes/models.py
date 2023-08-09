from django.db import models


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
    tags = models.ForeignKey(
        Tag,
        null=True, # Временно. Не может быть нулевым.
        on_delete=models.SET_NULL,
        related_name='recipes')
    """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes')
    """
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
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True)
    measurement_unit = models.CharField(
        max_length=200)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE)
