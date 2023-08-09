from django.contrib import admin

from .models import Tag, Recipe, Ingredient, RecipeIngredient


admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
