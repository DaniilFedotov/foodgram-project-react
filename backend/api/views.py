from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from recipes.models import Tag, Recipe, Ingredient
from users.models import User
from .serializers import (TagSerializer,
                          RecipeSerializer,
                          CreateRecipeSerializer,
                          IngredientSerializer,
                          UserSerializer,
                          CreateUserSerializer)
from .pagination import Pagination


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        return CreateRecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request):
        return None

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request):
        return None

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        return None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return UserSerializer
        return CreateUserSerializer
