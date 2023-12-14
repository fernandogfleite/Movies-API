from api.apps.movies.views.movies import (
    MovieViewSet,
    GenreViewSet
)

from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'movies', MovieViewSet, basename='movies')
router.register(r'genres', GenreViewSet, basename='genres')


urlpatterns = [
    path('', include(router.urls))
]