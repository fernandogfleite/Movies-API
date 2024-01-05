from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid


class Unaccent(models.Transform):
    bilateral = True
    lookup_name = 'unaccent'

    def as_postgresql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return "UNACCENT(%s)" % lhs, params


models.CharField.register_lookup(Unaccent)
models.TextField.register_lookup(Unaccent)


class BaseModel(models.Model):
    """
    Base model for all models in the project
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Movie(BaseModel):
    """
    Model for movies
    """
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(_('Name'),max_length=255)
    description = models.TextField(_('Description'))
    genres = models.ManyToManyField('Genre', through='MovieGenre', related_name='movies')
    rating = models.IntegerField(_('Rating'))
    duration = models.IntegerField(_('Duration'))
    image_url = models.URLField(_('Image URL'))
    released_at = models.DateField(_('Released At'))
    
    class Meta:
        verbose_name = _('Movie')
        verbose_name_plural = _('Movies')
        db_table = 'movies'
        
    def __str__(self):
        return self.name


class Genre(BaseModel):
    """
    Model for genres
    """
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(_('Name'),max_length=255)
    
    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        db_table = 'genres'
        
    def __str__(self):
        return self.name
    
    
class MovieGenre(BaseModel):
    """
    Model for connecting movies and genres
    """
    
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = _('Movie Genre')
        verbose_name_plural = _('Movie Genres')
        db_table = 'movie_genres'
        
    def __str__(self):
        return f"{self.movie.name} - {self.genre.name}"
