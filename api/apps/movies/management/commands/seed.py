from api.apps.movies.models.movies import (
    Genre,
    Movie
)

from django.core.management.base import BaseCommand
from django.db import transaction

from decouple import config
from datetime import datetime
from time import sleep
import requests



class TMDBClient:
    """
    Client for The Movie Database API
    """
    def __init__(self):
        self.headers = {
            'accept': 'application/json',
            'Authorization': f'Bearer {config("TMDB_TOKEN")}'
        }
    
    def get_genres(self):
        """
        Get all genres from The Movie Database API
        """
        url = f'https://api.themoviedb.org/3/genre/movie/list?language=pt-BR'
        response = requests.get(url, headers=self.headers)
        
        return response.json()
    
    def get_movies(self, quantity):
        """
        Get movies from The Movie Database API
        """
        url = f'https://api.themoviedb.org/3/movie/popular?language=pt-BR'
        movies = []
        
        for page in range(1, quantity + 1):
            response = requests.get(f'{url}&page={page}', headers=self.headers)
            movies += response.json()['results']
            sleep(0.25)
        
        return movies

    def get_movie_runtime(self, movie_id):
        """
        Get movie runtime from The Movie Database API
        """
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?language=pt-BR'
        response = requests.get(url, headers=self.headers)
        
        return response.json()['runtime']


class Command(BaseCommand):
    help = 'Seed database with initial data'
    
    def add_arguments(self, parser):
        parser.add_argument('quantity', type=int, help='Quantity of pages to get from The Movie Database API')
    
    @transaction.atomic
    def handle(self, *args, **options):
        quantity = options['quantity']
        
        client = TMDBClient()
        
        print('Seeding genres...')
        
        client_genres = client.get_genres()
        
        genre_dict = dict()
        
        for genre in client_genres['genres']:
            genre_instance = Genre.objects.create(
                name=genre['name']
            )
            genre_dict[genre['id']] = genre_instance
        
        print('Genres seeded!')
        
        print('Seeding movies...')
        
        client_movies = client.get_movies(quantity)
        
        for movie in client_movies:
            try:
                released_at = datetime.strptime(movie['release_date'], '%Y-%m-%d')
                movie_instance = Movie.objects.create(
                    name=movie['title'],
                    description=movie['overview'],
                    rating=movie['vote_average'],
                    duration=client.get_movie_runtime(movie['id']),
                    image_url=f"https://image.tmdb.org/t/p/w500{movie['poster_path']}",
                    released_at=released_at
                )
            except Exception as error:
                print(error)
                continue
            
            for genre in movie['genre_ids']:
                movie_instance.genres.add(genre_dict[genre])
                
            sleep(0.2)

        print('Movies seeded!')
