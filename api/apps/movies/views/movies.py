from api.apps.movies.models.movies import (
    Movie, 
    Genre
)
from api.apps.movies.serializers.movies import (
    MovieSerializer,
    GenreSerializer
)

from django.db.models import Q

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.permissions import AllowAny

from functools import reduce
import operator


class GenreViewSet(ReadOnlyModelViewSet):
    """
    Viewset for genres
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = Q()
        
        if self.action == 'list':
            name = self.request.query_params.get('name')
            
            if name:
                query &= reduce(
                    operator.__and__, 
                    (
                        Q(name__unaccent__icontains=name) for name in name.split(' ')
                    )
                )
        
        return queryset.filter(query).order_by('name')


class MovieViewSet(ReadOnlyModelViewSet):
    """
    Viewset for movies
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = (AllowAny,)
    
    def get_queryset(self):
        queryset = super().get_queryset()
        query = Q()
        
        if self.action == 'list':
            name = self.request.query_params.get('name')
            genre = self.request.query_params.get('genre')
            release_year = self.request.query_params.get('release_year')
            
            if name:
                query &= reduce(
                    operator.__and__, 
                    (
                        Q(name__unaccent__icontains=name) for name in name.split(' ')
                    )
                )
            
            if genre:
                query &= Q(
                    genres__id=genre
                )
                
            if release_year:
                query &= Q(
                    released_date__year=release_year
                )
        
        return queryset.filter(query).order_by('name')
