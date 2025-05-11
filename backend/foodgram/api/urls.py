from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (IngredientViewSet, RecipeViewSet, TagsViewSet,
                       UsersProfileViewSet)

router = SimpleRouter()
router.register('users', UsersProfileViewSet, basename='users')
# router.register('users/subscriptions',, basename='subscriptions')
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

auth_urls = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
urlpatterns = [
    path('', include(router.urls)),
    path('', include(auth_urls)),
]
