from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

from users.models import User


class Tag(models.Model):
    """Модель тегов."""
    name = models.CharField(
        max_length=settings.NAME_MAX_LEN,
        unique=True,
        verbose_name='Название тега',
        help_text='Название тега',
    )

    color = models.CharField(
        max_length=settings.COLOR_MAX_LEN,
        unique=True,
        verbose_name='Цветовой HEX-код',
        help_text='Цветовой HEX-код',
    )

    slug = models.SlugField(
        max_length=settings.SLUG_MAX_LEN,
        unique=True,
        verbose_name='Slug',
        help_text='Slug',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Ingredient(models.Model):
    """Модель ингредиентов."""
    name = models.CharField(
        max_length=settings.NAME_MAX_LEN,
        verbose_name='Название ингредиента',
        help_text='Название ингредиента',
    )

    measurement_unit = models.CharField(
        max_length=settings.UNIT_MAX_LEN,
        verbose_name='Измеряемая единица',
        help_text='Измеряемая единица',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    """Модель рецептов."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор',
        help_text='Автор'
    )

    name = models.CharField(
        max_length=settings.NAME_MAX_LEN,
        verbose_name='Название рецепта',
        help_text='Название рецепта',
    )

    text = models.TextField(
        verbose_name='Описание рецепта',
        help_text='Описание рецепта',
    )

    image = models.ImageField(
        verbose_name='Фото блюда',
        help_text='Фото блюда',
        upload_to='recipes/img/',
    )

    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время готовки(минуты)',
        help_text='Время готовки(минуты)',
        validators=(MinValueValidator(settings.COOKING_TIME_MIN_VALUE), )
    )

    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    tags = models.ManyToManyField(Tag, related_name='recipes',
                                  verbose_name='Теги',
                                  through='TagRecipe')

    ingredients = models.ManyToManyField(Ingredient, related_name='recipes',
                                         verbose_name='Ингредиенты',
                                         through='IngredientRecipe')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class TagRecipe(models.Model):
    """Модель связи М:М тегов и рецептов."""
    tag = models.ForeignKey(Tag, related_name='tag_recipes',
                            verbose_name='Тег',
                            on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, related_name='tags_recipe',
                               verbose_name='Рецепт',
                               on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.recipe}'

    class Meta:
        verbose_name = 'Тег-Рецепт'
        verbose_name_plural = 'Теги-Рецепты'


class IngredientRecipe(models.Model):
    """Модель связи М:М ингредиентов и рецептов."""
    ingredient = models.ForeignKey(Ingredient,
                                   related_name='ingredient_recipes',
                                   verbose_name='Ингредиент',
                                   help_text='Ингредиент',
                                   on_delete=models.PROTECT)
    recipe = models.ForeignKey(Recipe, related_name='ingredients_recipe',
                               verbose_name='Рецепт',
                               help_text='Рецепт',
                               on_delete=models.CASCADE)
    amount = models.PositiveSmallIntegerField(
        verbose_name='Кол-во ингредиента',
        help_text='Кол-во ингредиента',
        validators=(MinValueValidator(settings.AMOUNT_MIN_VALUE), )
    )

    def __str__(self):
        return f'{self.ingredient} {self.recipe}  {self.amount}'

    class Meta:
        verbose_name = 'Ингредиент-Рецепт'
        verbose_name_plural = 'Ингредиенты-Рецепты'


class Favorite(models.Model):
    """Модель связи рецептов и пользователей."""
    recipe = models.ForeignKey(Recipe, related_name='favorites_recipe',
                               verbose_name='Рецепт',
                               help_text='Рецепт',
                               on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='favorites_user',
                             verbose_name='Пользователь',
                             help_text='Пользователь',
                             on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe} {self.user}'

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=('recipe', 'user'),
                                    name='unique_favorit'),
        )
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class ShoppingCart(models.Model):
    """Модель связи списков покупок и пользователей."""
    recipe = models.ForeignKey(Recipe, related_name='shopping_cart_recipe',
                               verbose_name='Рецепт',
                               help_text='Рецепт',
                               on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='shopping_cart_user',
                             verbose_name='Пользователь',
                             help_text='Пользователь',
                             on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.recipe} {self.user}'

    class Meta:
        constraints = (
            models.UniqueConstraint(fields=('recipe', 'user'),
                                    name='unique_shopping_cart'),
        )
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
