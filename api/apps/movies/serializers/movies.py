from api.apps.movies.models.movies import (
    Movie, 
    Genre
)

from rest_framework import serializers


class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer for genres
    """
    
    class Meta:
        model = Genre
        fields = (
            'id',
            'name'
        )
        

class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for movies
    """
    genres = GenreSerializer(many=True, read_only=True)
    
    class Meta:
        model = Movie
        fields = (
            'id',
            'name',
            'description',
            'genres',
            'rating',
            'duration',
            'image',
            'released_at'
        )
