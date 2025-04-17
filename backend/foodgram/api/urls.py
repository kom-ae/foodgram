from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import FoodGramUsersViewSet

router = SimpleRouter()
# router.register('users', FoodGramUsersViewSet, basename='users')

auth_urls = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken'))
]
urlpatterns = [
    # path('', include(router.urls)),
    path('users/me/avatar/', FoodGramUsersViewSet.as_view({'put': 'update'})),
    path('users/<int:pk>/', FoodGramUsersViewSet.as_view({'get': 'retrieve'})),
    path('users/', FoodGramUsersViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('', include(auth_urls)),
]
