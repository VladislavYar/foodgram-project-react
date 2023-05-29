from app.models import Recipe, Tag
from django_filters import FilterSet, ModelMultipleChoiceFilter, NumberFilter
from rest_framework.filters import SearchFilter


class RecipeFilter(FilterSet):
    """Фильтр рецептов."""
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug')
    is_favorited = NumberFilter(field_name='favorit_recipe__user',
                                method='is_favorited_filter')
    is_in_shopping_cart = NumberFilter(field_name='shopping_cart_recipe__user',
                                       method='is_in_shopping_cart_filter')

    class Meta:
        model = Recipe
        fields = ('author', 'tags', )

    def is_favorited_filter(self, queryset, name, value):
        """Фильтр рецпта по избранному."""
        if value == 1:
            return queryset.filter(**{
                name: self.request.user,
            })
        return queryset

    def is_in_shopping_cart_filter(self, queryset, name, value):
        """Фильтр рецпта по списку покупок."""
        if value == 1:
            return queryset.filter(**{
                name: self.request.user,
            })
        return queryset


class IngredientSearchFilter(SearchFilter):
    """Изменяет назнавие параметра для поиска."""
    search_param = ('name')
