from django.contrib import admin

from .models import (Tag,
                     Recipe,
                     Ingredient,
                     RecipeIngredient,
                     RecipeTag,
                     Favorites,
                     ShoppingCart)


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author__username',)
    list_filter = ('author__username', 'name', 'tags__name',)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


admin.site.register(Tag)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeTag)
admin.site.register(Favorites)
admin.site.register(ShoppingCart)
