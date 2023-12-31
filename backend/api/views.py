from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Sum

from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from djoser.views import UserViewSet

from recipes.models import (Tag, Recipe, Ingredient, Favorites, ShoppingCart)
from users.models import User, Subscriptions
from .serializers import (TagSerializer,
                          SpecialRecipeSerializer,
                          IngredientSerializer,
                          CustomUserSerializer,
                          CustomCreateUserSerializer,
                          SubscriptionsSerializer,
                          RecipeSerializer)
from .pagination import Pagination
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly


class RecipeViewSet(ModelViewSet):
    """Вьюсет для модели рецепта."""
    queryset = Recipe.objects.all()
    pagination_class = Pagination
    permission_classes = (IsAuthorOrReadOnly | IsAdminOrReadOnly,)
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        """Функция сохранения пользователя как автора при создании рецепта."""
        serializer.save(author=self.request.user)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        """Функция добавления рецепта в избранное."""
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, id=pk)
            Favorites.objects.create(user=request.user, recipe=recipe)
            serializer = SpecialRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        favorite = Favorites.objects.filter(user=request.user, recipe__id=pk)
        if favorite.exists():
            favorite.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        """Функция добавления рецепта в продуктовую корзину."""
        if request.method == 'POST':
            recipe = get_object_or_404(Recipe, id=pk)
            if ShoppingCart.objects.filter(user=request.user,
                                           recipe=recipe).exists():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.create(user=request.user, recipe=recipe)
            serializer = SpecialRecipeSerializer(recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        cart = ShoppingCart.objects.filter(user=request.user, recipe__id=pk)
        if cart.exists():
            cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Функция загрузки продуктовой корзины пользователя."""
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = Ingredient.objects.filter(
            recipe__recipe__shopping_cart__user=user).values(
            'name',
            'measurement_unit').annotate(amount=Sum('recipe__amount'))
        shopping_list = ['Список покупок.']
        for ingredient in ingredients:
            shopping_list += [
                f'{ingredient["name"]}'
                f'({ingredient["measurement_unit"]}):'
                f'{ingredient["amount"]}']
        filename = f'{user.username}_shopping_list.txt'
        result_list = '\n'.join(shopping_list)
        response = HttpResponse(result_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class TagViewSet(ReadOnlyModelViewSet):
    """Вьюсет для модели тега."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    """Вьюсет для модели ингредиента."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)


class CustomUserViewSet(UserViewSet):
    """Вьюсет для модели пользователя."""
    queryset = User.objects.all()
    pagination_class = Pagination

    def get_serializer_class(self):
        """Функция получения нужного сериализатора."""
        if self.request.method == 'GET':
            return CustomUserSerializer
        return CustomCreateUserSerializer

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, **kwargs):
        """Функция подписки на пользователя."""
        user = request.user
        author = get_object_or_404(User, id=self.kwargs.get('id'))
        if request.method == 'POST':
            serializer = SubscriptionsSerializer(author,
                                                 data=request.data,
                                                 context={'request': request})
            serializer.is_valid(raise_exception=True)
            Subscriptions.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        subscription = get_object_or_404(Subscriptions,
                                         user=user,
                                         author=author)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False,
            methods=['get'],
            permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        """Функция выдачи пользователей, на которых подписан автор запроса."""
        user = request.user
        subscribers = User.objects.filter(subscribers__user=user)
        pages = self.paginate_queryset(subscribers)
        serializer = SubscriptionsSerializer(
            pages,
            many=True,
            context={'request': request})
        return self.get_paginated_response(serializer.data)
