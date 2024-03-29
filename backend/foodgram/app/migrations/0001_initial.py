# Generated by Django 4.2.1 on 2023-06-06 15:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название ингредиента', max_length=200, verbose_name='Название ингредиента')),
                ('measurement_unit', models.CharField(help_text='Измеряемая единица', max_length=200, verbose_name='Измеряемая единица')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveSmallIntegerField(help_text='Кол-во ингредиента', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Кол-во ингредиента')),
                ('ingredient', models.ForeignKey(help_text='Ингредиент', on_delete=django.db.models.deletion.PROTECT, related_name='ingredient_recipes', to='app.ingredient', verbose_name='Ингредиент')),
            ],
            options={
                'verbose_name': 'Ингредиент-Рецепт',
                'verbose_name_plural': 'Ингредиенты-Рецепты',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название рецепта', max_length=200, verbose_name='Название рецепта')),
                ('text', models.TextField(help_text='Описание рецепта', verbose_name='Описание рецепта')),
                ('image', models.ImageField(help_text='Фото блюда', upload_to='recipes/img/', verbose_name='Фото блюда')),
                ('cooking_time', models.PositiveSmallIntegerField(help_text='Время готовки(минуты)', validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время готовки(минуты)')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(help_text='Автор', on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('ingredients', models.ManyToManyField(related_name='recipes', through='app.IngredientRecipe', to='app.ingredient', verbose_name='Ингредиенты')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Название тега', max_length=200, unique=True, verbose_name='Название тега')),
                ('color', models.CharField(help_text='Цветовой HEX-код', max_length=7, unique=True, verbose_name='Цветовой HEX-код')),
                ('slug', models.SlugField(help_text='Slug', max_length=200, unique=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='TagRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags_recipe', to='app.recipe', verbose_name='Рецепт')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tag_recipes', to='app.tag', verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'Тег-Рецепт',
                'verbose_name_plural': 'Теги-Рецепты',
            },
        ),
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(help_text='Рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart_recipe', to='app.recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(help_text='Пользователь', on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Списки покупок',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(related_name='recipes', through='app.TagRecipe', to='app.tag', verbose_name='Теги'),
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(help_text='Рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='ingredients_recipe', to='app.recipe', verbose_name='Рецепт'),
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(help_text='Рецепт', on_delete=django.db.models.deletion.CASCADE, related_name='favorites_recipe', to='app.recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(help_text='Пользователь', on_delete=django.db.models.deletion.CASCADE, related_name='favorites_user', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Избранное',
                'verbose_name_plural': 'Избранное',
            },
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='unique_shopping_cart'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('recipe', 'user'), name='unique_favorit'),
        ),
    ]
