from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import UsersViewSet, UsersProfileViewSet

router = SimpleRouter()
router.register('users', UsersProfileViewSet, basename='users')

auth_urls = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken'))
]
urlpatterns = [
    path('', include(router.urls)),

    # path('users/me/<str:param>/', FoodGramUsersViewSet.as_view({'put': 'update'})),
    # path('users/<int:pk>/', FoodGramUsersProfileViewSet.as_view({'get': 'retrieve'})),

    # path('users/me/avatar/', UsersProfileViewSet.as_view({'put': 'update'})),
    # path('users/me/', UsersProfileViewSet.as_view),
    # path('users/<int:id>/', UsersProfileViewSet.as_view({'get': 'retrieve'})),
    # path('users/', UsersProfileViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('', include(auth_urls)),
]
