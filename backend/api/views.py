from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from recipes.models import Tag, Recipe, Ingredient
from users.models import User
from .serializers import (TagSerializer,
                          RecipeSerializer,
                          GetRecipeSerializer,
                          IngredientSerializer,
                          UserSerializer,
                          GetUserSerializer,
                          SignUpSerializer,
                          GetJwtTokenSerializer)
from .pagination import Pagination


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetRecipeSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = Pagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetUserSerializer
        return UserSerializer


def get_tokens_for_user(user):
    """Обновление пары токенов для пользователя."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }
