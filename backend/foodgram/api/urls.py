from django.urls import include, path

from api.views import FoodGramUsersViewSet


auth_urls = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken'))
]
urlpatterns = [
    path('', include(auth_urls)),
    path('user1/', FoodGramUsersViewSet.as_view({'get': 'list'}))
]
