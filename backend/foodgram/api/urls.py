from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import TagsViewSet, UsersProfileViewSet, IngredientViewSet

router = SimpleRouter()
router.register('users', UsersProfileViewSet, basename='users')
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientViewSet, basename='ingredients')

auth_urls = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken'))
]
urlpatterns = [
    path('', include(router.urls)),
    path('', include(auth_urls)),
]
