from api.apps.movies.views.movies import (
    MovieViewSet,
    GenreViewSet,
    ReleaseYearsAPIView
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
    path('movies/release-years/', ReleaseYearsAPIView.as_view(), name='release-years'),
    path('', include(router.urls)),
]