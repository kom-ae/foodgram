from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import UsersProfileViewSet, TagsViewSet

router = SimpleRouter()
router.register('users', UsersProfileViewSet, basename='users')
router.register('tags', TagsViewSet, basename='tags')

auth_urls = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken'))
]
urlpatterns = [
    path('', include(router.urls)),
    path('', include(auth_urls)),
]
