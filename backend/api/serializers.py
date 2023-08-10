from rest_framework import serializers

from recipes.models import Tag, Recipe, Ingredient, RecipeIngredient, RecipeTag
from users.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id',)


class GetTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id',)  # 'measurement_unit',


class GetIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name')  # 'measurement_unit',


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'name', 'text', 'cooking_time')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        for tag in tags:
            current_tag, status = Tag.objects.get_or_create(**tag)
            RecipeTag.objects.create(recipe=recipe, tag=current_tag)
        for ingredient in ingredients:
            current_ingredient, status = Ingredient.get_or_create(**ingredient)
            RecipeIngredient.objects.create(recipe=recipe, ingredient=current_ingredient)
        return recipe


class GetRecipeSerializer(serializers.ModelSerializer):
    tags = GetTagSerializer(read_only=True, many=True)
    ingredients = IngredientSerializer(read_only=True, many=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'text', 'cooking_time')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password',)


class SignUpSerializer(serializers.Serializer):
    """Сериализатор регистрации пользователей."""
    username = serializers.CharField(
        max_length=150,
        required=True,)
    email = serializers.EmailField(
        max_length=256,
        required=True,)


class GetJwtTokenSerializer(serializers.Serializer):
    """Сериализатор получения токена."""
    username = serializers.CharField(
        max_length=150,)
    confirmation_code = serializers.CharField()
