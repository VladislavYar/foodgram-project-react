from django.contrib import admin

from app.models import (Favorite, Ingredient, IngredientRecipe, Recipe,
                        ShoppingCart, Tag, TagRecipe)


class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug', )
    list_editable = ('name', 'color', 'slug', )
    empty_value_display = '-пусто-'


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name', 'measurement_unit')
    list_filter = ('name', )
    list_editable = ('name', )
    empty_value_display = '-пусто-'


class TagRecipeInline(admin.TabularInline):
    model = TagRecipe
    extra = 1


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipe
    extra = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'name', 'text',
                    'image', 'cooking_time', 'pub_date',
                    'get_tags', 'get_ingredients', 'get_count_favorite')
    inlines = (TagRecipeInline, IngredientRecipeInline, )
    search_fields = ('author__username', 'name', )
    list_filter = ('author', 'name', 'tags__name', )
    list_editable = ('name', )
    empty_value_display = '-пусто-'

    def get_tags(self, obj):
        return ", ".join([tag.slug for tag in obj.tags.all()])

    get_tags.short_description = 'Теги'

    def get_ingredients(self, obj):
        return ", ".join(
            [ingredient.name for ingredient in obj.ingredients.all()]
            )

    get_ingredients.short_description = 'Ингредиенты'

    def get_count_favorite(self, obj):
        """Кол-во добавлений рецепта в избранное."""
        return Favorite.objects.filter(recipe=obj.pk).count()

    get_count_favorite.short_description = ('Кол-во в избранном')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'user')
    search_fields = ('recipe', 'user', )
    empty_value_display = '-пусто-'


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'user')
    search_fields = ('recipe', 'user', )
    empty_value_display = '-пусто-'


class TagRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'tag')
    search_fields = ('recipe', 'tag', )
    empty_value_display = '-пусто-'


class IngredientRecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    search_fields = ('recipe', 'ingredient', )
    empty_value_display = '-пусто-'


admin.site.register(Tag, TagAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(TagRecipe, TagRecipeAdmin)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
