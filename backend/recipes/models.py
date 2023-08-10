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
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Название ингредиента')
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения ингредиента')

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE)
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'tag'], name='recipetag_unique')]

    def __str__(self):
        return f'Рецепт {self.recipe} имеет тег {self.tag}'


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт')
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент')
    amount = models.PositiveIntegerField(
        verbose_name='Количество')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'], name='recipeingredient_unique')]

    def __str__(self):
        return f'Рецепт {self.recipe} содержит {self.ingredient}'


class RecipeUser(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт')
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'], name='recipeuser_unique')]

    def __str__(self):
        return f'Рецепт {self.recipe} в избранном {self.user}'