import base64

from django.db import transaction
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.files.base import ContentFile
from rest_framework import serializers

from app.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                        ShoppingCart, Tag, TagRecipe)
from core.validators import (validate_favorite_shopping_cart,
                             validate_subscribe, validate_tags_ingredients,
                             validate_amount, validate_cooking_time, )
from users.models import Subscribe, User


class UserSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')

    class Meta:
        fields = ('id', 'email',  'username', 'first_name',
                  'last_name', 'is_subscribed', )
        model = User

    def get_is_subscribed(self, obj):
        """Возвращает bool значение подписки текущего пользователя."""
        return Subscribe.objects.filter(
            author=obj.pk, user=self.context.get('request').user.pk).exists()


class UserRegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'email',  'username', 'first_name',
                  'last_name',  'password', )
        model = User
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        """Сохраняет захешированный пароль."""
        validated_data['password'] = make_password(validated_data.
                                                   get('password'))
        return super().create(validated_data)


class UserSubscribeSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')

    class Meta:
        fields = ('id', 'email',  'username', 'first_name',
                  'last_name', 'is_subscribed', 'recipes_count')
        model = User

    def get_is_subscribed(self, obj):
        """Возвращает bool значение подписки текущего пользователя."""
        user_pk = self.context.get('request').user.pk
        return Subscribe.objects.filter(author=obj.pk, user=user_pk).exists()

    def get_recipes_count(self, obj):
        """Возвращает кол-во рецептов автора."""
        return obj.recipes.count()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'color', 'slug', )
        model = Tag


class TagRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('recipe', 'tag', )
        model = TagRecipe


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'measurement_unit', )
        model = Ingredient
        extra_kwargs = {
            'name': {'read_only': True},
            'measurement_unit': {'read_only': True},
        }


class IngredientAmountSerializer(serializers.Serializer):

    amount = serializers.IntegerField()
    id = serializers.ModelField(model_field=Ingredient(
                                )._meta.get_field('id'))

    def validate_amount(self, data):
        return validate_amount(data, settings.AMOUNT_MIN_VALUE,
                               settings.AMOUNT_MAX_VALUE,
                               'Количество ингредиента')


class IngredientRecipeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('recipe', 'ingredient', 'amount', )
        model = IngredientRecipe


class Base64ImageField(serializers.ImageField):
    """Преобразует base64-строку в изображение."""
    def to_internal_value(self, data):
        try:
            format, data = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(data), name='temp.' + ext)
        except (ValueError, AttributeError):
            data = 'no correct'
        return super().to_internal_value(data)


class RecipeReadOnlyFavoriteShoppingSubscribeSerializer(
      serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'image', 'cooking_time', )
        model = Recipe


class RecipePATCHSerializer(serializers.ModelSerializer):
    """Serializer для валидации полей PATCH-запроса."""

    tags = serializers.ListField(required=True)
    ingredients = IngredientAmountSerializer(many=True, required=True)

    class Meta:
        fields = ('ingredients', 'tags', 'name', 'image',
                  'text', 'cooking_time', )
        model = Recipe


class RecipeReadOnlySerializer(serializers.ModelSerializer):

    is_favorited = serializers.SerializerMethodField('get_is_favorited')
    is_in_shopping_cart = (
        serializers.SerializerMethodField('get_is_in_shopping_cart')
        )
    tags = TagSerializer(many=True)
    ingredients = IngredientSerializer(many=True)
    author = UserSerializer()

    class Meta:
        fields = (
            'id', 'author', 'ingredients', 'tags', 'name', 'image',
            'text', 'cooking_time', 'is_favorited', 'is_in_shopping_cart',
            )
        model = Recipe

    def get_is_favorited(self, obj):
        """Возвращает bool значение нахождения рецепта в избранном."""
        user_pk = self.context.get('request').user.pk
        return Favorite.objects.filter(recipe=obj.pk, user=user_pk).exists()

    def get_is_in_shopping_cart(self, obj):
        """Возвращает bool значение нахождения рецепта в списке покупок."""
        user_pk = self.context.get('request').user.pk
        return ShoppingCart.objects.filter(recipe=obj.pk,
                                           user=user_pk).exists()


class RecipeSerializer(serializers.ModelSerializer):

    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all())
    ingredients = IngredientAmountSerializer(many=True)
    image = Base64ImageField()
    cooking_time = serializers.IntegerField()

    class Meta:
        fields = (
            'id', 'author', 'ingredients', 'tags', 'name', 'image',
            'text', 'cooking_time',
            )
        model = Recipe
        extra_kwargs = {
            'author': {'read_only': True},
        }

    def _delete_old_tags_or_ingredients(self, recipe, name_field):
        """Удаляет старые записи M:M рецепты-(теги, ингредиенты)
            при PATCH-запросе."""
        metod = self.context.get('request').method
        if metod == 'PATCH':
            if name_field == 'ingredient':
                recipe.ingredients_recipe.all().delete()
            if name_field == 'tag':
                recipe.tags_recipe.all().delete()

    def _save_tags_or_ingredients(self, serializer, data,
                                  name_field, recipe):
        """Сохраняет(обновляет) данные тегов и ингредиентов."""
        if name_field == 'ingredient':
            for field in data:
                new_ingredient = {'recipe': recipe.pk, name_field:
                                  field.get('id')}
                field.pop('id')
                field.update(new_ingredient)
        if name_field == 'tag':
            data = [{'recipe': recipe.pk, name_field: field.pk}
                    for field in data]

        data = serializer(data=data, many=True)
        data.is_valid(raise_exception=True)

        self._delete_old_tags_or_ingredients(recipe, name_field)

        data.save()

    def _summ_values_same_fields(self, ingredients):
        """Суммуриует значения поля 'amount' одинаковых ингредиентов."""
        id = []
        amount = []
        for ingredient in ingredients:
            id.append(ingredient.get('id'))
            amount.append(ingredient.get('amount'))

        id_amount = {}
        index = 0
        for one_id in id:
            if one_id in id_amount:
                id_amount[one_id] += amount[index]
            else:
                id_amount[one_id] = amount[index]
            index += 1

        ingredients = []
        [ingredients.append({'id': key, 'amount': value})
         for key, value in id_amount.items()]
        return ingredients

    @transaction.atomic
    def create(self, validated_data):
        """Сохраняет рецепт в базе."""
        obj = Recipe.objects.create(author=self.context.get('request').user,
                                    name=validated_data['name'],
                                    image=validated_data['image'],
                                    text=validated_data['text'],
                                    cooking_time=validated_data['cooking_time']
                                    )

        ingredients = self._summ_values_same_fields(validated_data.pop(
                                                    'ingredients'))
        self._save_tags_or_ingredients(IngredientRecipeSerializer, ingredients,
                                       'ingredient', obj)

        tags = list(set(validated_data.pop('tags')))
        self._save_tags_or_ingredients(TagRecipeSerializer, tags, 'tag', obj)

        return obj

    @transaction.atomic
    def update(self, instance, validated_data):
        """Обновляет рецепт в базе."""
        instance.name = validated_data.get('name')
        instance.text = validated_data.get('text')
        instance.cooking_time = validated_data.get('cooking_time')

        new_image = validated_data.get('image')
        if new_image:
            instance.image = validated_data.get('image')

        ingredients = self._summ_values_same_fields(validated_data.pop(
                                                    'ingredients'))
        self._save_tags_or_ingredients(IngredientRecipeSerializer,
                                       ingredients, 'ingredient',
                                       instance)

        tags = validated_data.pop('tags')
        self._save_tags_or_ingredients(TagRecipeSerializer, tags, 'tag',
                                       instance)

        instance.save()
        return instance

    def to_representation(self, obj):
        """Добавляет к ингредиентам поле кол-ва."""
        data = RecipeReadOnlySerializer(
            obj, context={'request': self.context.get('request')}).data
        ingredients = data.get('ingredients')
        for ingredient in ingredients:
            ingredient['amount'] = (
                    IngredientRecipe.objects.get(
                        recipe=data.get('id'), ingredient=ingredient.get('id')
                        ).amount
                 )
        return data

    def validate_tags(self, data):
        return validate_tags_ingredients(data)

    def validate_ingredients(self, data):
        return validate_tags_ingredients(data)

    def validate_cooking_time(self, data):
        return validate_cooking_time(data, settings.COOKING_TIME_MIN_VALUE,
                                     settings.COOKING_TIME_MAX_VALUE,
                                     'Время готовки')

    def validate(self, data):
        """Валидирует поля при PATCH-запросе."""
        if self.context.get('request').method == 'PATCH':
            RecipePATCHSerializer(data=data).is_valid(raise_exception=True)
        return data


class SubscribeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = '__all__'
        extra_kwargs = {
            'user': {'required': False},
            'author': {'required': False},
        }

    def _get_recipes_limit(self):
        """Получает кол-во выводимых рецептов из параметра."""
        try:
            recipes_limit = int(self.context.get(
                'request').query_params.get('recipes_limit'))
        except (ValueError, TypeError):
            recipes_limit = None
        return recipes_limit

    def to_representation(self, obj):
        """Возвращает автора, на которого подписались."""
        recipes_limit = self._get_recipes_limit()
        recipes = RecipeReadOnlyFavoriteShoppingSubscribeSerializer(
            obj.author.recipes.all()[:recipes_limit], many=True
        ).data
        data = UserSubscribeSerializer(obj.author,
                                       context={'request': obj}).data
        data['recipes'] = recipes
        return data

    def validate(self, data):
        return validate_subscribe(self.context)


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('recipe', 'user', )
        model = Favorite

    def to_representation(self, obj, ):
        """Возвращает добавленный рецепт в избранное."""
        return RecipeReadOnlyFavoriteShoppingSubscribeSerializer(
               obj.recipe).data

    def validate(self, data):
        message = 'избранных'
        return validate_favorite_shopping_cart(data, self.context['request'],
                                               Favorite, message)


class ShoppingCartSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('recipe', 'user', )
        model = ShoppingCart

    def to_representation(self, obj):
        """Возвращает добавленный рецепт в список покупок."""
        return RecipeReadOnlyFavoriteShoppingSubscribeSerializer(
               obj.recipe).data

    def validate(self, data):
        message = 'покупок'
        return validate_favorite_shopping_cart(data, self.context['request'],
                                               ShoppingCart, message)
