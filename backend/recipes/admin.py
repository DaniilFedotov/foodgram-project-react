from django.contrib import admin

from .models import (Tag,
                     Recipe,
                     Ingredient,
                     RecipeIngredient,
                     RecipeTag,
                     Favorites,
                     ShoppingCart)


admin.site.register(Tag)
admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient)
admin.site.register(RecipeTag)
admin.site.register(Favorites)
admin.site.register(ShoppingCart)
