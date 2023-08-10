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
from foodgram.settings import ADMIN_EMAIL


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


@api_view(['POST'])
def sign_up_user(request):
    """Функция регистрации пользователей."""
    serializer = SignUpSerializer(data=request.data)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    try:
        current_user, _ = User.objects.get_or_create(email=email, username=username)
    except IntegrityError:
        raise serializers.ValidationError('Такой пользователь уже существует')
    confirm_code = default_token_generator.make_token(current_user)
    send_mail('Confirmation of registration',
              f'your code: {confirm_code}',
              ADMIN_EMAIL,
              [email],
              fail_silently=False,)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_jwt_token(request):
    """Функция получения токена."""
    serializer = GetJwtTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data['confirmation_code']
    username = serializer.validated_data.get('username')
    current_user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(current_user, confirmation_code):
        return Response(get_tokens_for_user(current_user))
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

