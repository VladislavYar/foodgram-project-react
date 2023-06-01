from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (IngredientViewSet, RecipeViewSet, SubscribeViewSet,
                       TagViewSet, ShoppingCartView)

app_name = 'api'

router = DefaultRouter()

router.register(r'tags', TagViewSet, basename='tags')
router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('recipes/download_shopping_cart/', ShoppingCartView.as_view()),
    path('users/<int:id>/subscribe/',
         SubscribeViewSet.as_view({'post': 'create', 'delete': 'destroy'})),
    path('users/subscriptions/', SubscribeViewSet.as_view({'get': 'list'})),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
