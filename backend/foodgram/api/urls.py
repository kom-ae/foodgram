from django.urls import include, path


auth_urls = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.authtoken'))
]
urlpatterns = [
    path('auth/', include(auth_urls)),
]
