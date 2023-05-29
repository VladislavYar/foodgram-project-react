from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeSerializer, ShoppingCartSerializer,
                             SubscribeSerializer, TagSerializer)
from app.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from core.actions import action_shopping_cart_fovorite
from core.filters import IngredientSearchFilter, RecipeFilter
from core.mixins import PDF, ListDestroyCreateModelViewSet
from core.permissions import (AuthorOrReadOnlyPermission,
                              ReadFileIsAuthenticatedPermission)
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from users.models import Subscribe


class SubscribeViewSet(ListDestroyCreateModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = SubscribeSerializer

    def get_queryset(self):
        """Отдаёт объекты для вывода."""
        user = self.request.user.pk
        return Subscribe.objects.filter(user=user, )

    def get_object(self):
        """Отдаёт объект для удаления."""
        author = self.kwargs.get('id')
        user = self.request.user.pk
        serializer = self.get_serializer(data={})
        serializer.is_valid(raise_exception=True)
        return get_object_or_404(Subscribe, author=author, user=user)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ('get', )


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (IngredientSearchFilter, )
    search_fields = ('name', )
    http_method_names = ('get', )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (AuthorOrReadOnlyPermission, )
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    http_method_names = ('get', 'post', 'patch', 'delete', )

    def get_permissions(self):
        """Изменяет permission при обращении к action
           с получением файла необходимых покупок."""
        if self.action == 'get_download_shopping_cart':
            return (ReadFileIsAuthenticatedPermission(), )
        return super(RecipeViewSet, self).get_permissions()

    @action(methods=('POST', 'DELETE', ),
            detail=True, url_path='favorite', url_name='favorite',)
    def post_del_favorite(self, request, pk):
        """Добавляет/удаляет рецепт в избранное."""
        return action_shopping_cart_fovorite(request, pk, FavoriteSerializer,
                                             Favorite)

    @action(methods=('POST', 'DELETE', ),
            detail=True, url_path='shopping_cart', url_name='shopping_cart',)
    def get_post_del_shopping_cart(self, request, pk):
        """Добавляет/удаляет рецепт в список покупок."""
        return action_shopping_cart_fovorite(request, pk,
                                             ShoppingCartSerializer,
                                             ShoppingCart)

    def _get_pdf_file_as_byte_str(self, info):
        """Отдаёт PDF-файл в виде байт-строки."""
        pdf = PDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        pdf.set_title('Ingredients')
        pdf.set_author('Yaremenko V.V.')
        pdf.set_font('CuprumRU', '', 14)

        line_number = 1
        pdf.cell(0, 10, txt='   Необходимые ингредиенты:', ln=1)
        for key, value in info.items():
            pdf.cell(0, 10, ln=1,
                     txt='         '
                         f'{line_number}) {key}({value[1]}) — {value[0]}',
                     )
            line_number += 1

        return pdf.output(dest='S').encode('latin-1')

    def _get_info_ingredients(self, request):
        """Получает информацию об ингредиентах в рецептах."""
        recipes = request.user.shopping_cart_user.all()
        info = {}
        for recipe in recipes:
            ingredients = recipe.recipe.ingredient_recipe.all()
            for ingredient in ingredients:
                measurement_unit = ingredient.ingredient.measurement_unit
                info.setdefault(ingredient.ingredient.name,
                                [0, measurement_unit])
                key = ingredient.ingredient.name
                info[key][0] += ingredient.amount
        return info

    @action(methods=('GET', ),
            detail=False, url_path='download_shopping_cart',
            url_name='download_shopping_cart', )
    def get_download_shopping_cart(self, request):
        """Отдаёт файл с необходимыми ингредиентами для покупки."""
        info = self._get_info_ingredients(request)
        pdf = self._get_pdf_file_as_byte_str(info)
        return HttpResponse(pdf, content_type='application/pdf')
