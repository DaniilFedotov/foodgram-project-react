from django.db.models import F

from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework.relations import PrimaryKeyRelatedField

from recipes.models import Tag, Recipe, Ingredient, RecipeIngredient, RecipeTag
from users.models import User, Subscriptions


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit',)
        read_only_fields = ('id', 'name', 'measurement_unit',)


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password',)


class UserSerializer(ModelSerializer):
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed',)
        read_only_fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed',)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return user.subscriptions.filter(author=obj).exists()


class RecipeSerializer(ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer(read_only=True)
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'text', 'cooking_time')
        read_onli_fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                            'is_in_shopping_cart', 'name', 'text', 'cooking_time')

    def get_ingredients(self, obj):
        ingredients = obj.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipe__amount'),)
        return ingredients

    def get_is_favorited(self, obj):
        user = self.context.get('view').request.user
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('view').request.user
        return user.shopping_cart.filter(recipe=obj).exists()


class CreateRecipeSerializer(ModelSerializer):
    tags = PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)

    class Meta:
        model = Recipe
        fields = ('ingredients', 'tags', 'name', 'text', 'cooking_time')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe, ingredients)
        return recipe

    def create_ingredients(self, recipe, ingredients):
        for ingredient_data in ingredients:
            ingredient = Ingredient.objects.get(id=ingredient_data['id'])
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=ingredient_data['amount'])


class SpecialRecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time')
        read_only_fields = ('id', 'name', 'cooking_time')


class SubscriptionsSerializer(UserSerializer):
    recipes = SpecialRecipeSerializer(many=True, read_only=True)
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()
