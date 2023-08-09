from rest_framework import viewsets

from recipes.models import Tag, Recipe, Ingredient
from .serializers import TagSerializer, RecipeSerializer, IngredientSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset =  Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer

