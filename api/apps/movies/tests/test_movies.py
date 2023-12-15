from api.apps.movies.models.movies import Movie, Genre
from api.apps.movies.serializers.movies import MovieSerializer

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status


RESOURCE_URL = reverse('movies:movies-list')

def detail_url(movie_id):
    """
    Return movie detail URL
    """
    
    return reverse('movies:movies-detail', args=[movie_id])


def sample_genre(name='Test Genre'):
    """
    Create a sample genre
    """
    
    return Genre.objects.create(name=name)


def sample_movie(name='Test Movie', 
                 description='Test Description', 
                 rating=5, 
                 duration=120, 
                 image_url='https://test.com/test.png', 
                 released_at='2020-01-01',
                 genre=None):
    """
    Create a sample movie
    """
    
    movie = Movie.objects.create(
        name=name,
        description=description,
        rating=rating,
        duration=duration,
        image_url=image_url,
        released_at=released_at
    )
    
    if genre:
        movie.genres.add(genre)
    
    return movie


class TestListMovies(APITestCase):
    def setUp(self):
        self.genre = sample_genre()
        genre_2 = sample_genre(name='Test Genre 2')
        
        sample_movie(genre=self.genre)
        sample_movie(genre=genre_2, released_at='2000-01-02', name='Moovie 2')
        
    
    def test_list_movies(self):
        """
        Test listing movies
        """
        movies = Movie.objects.all().order_by('name')
        serializer = MovieSerializer(movies, many=True)
        
        response = self.client.get(RESOURCE_URL)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'], serializer.data)
    
    def test_list_movies_filter_by_genre(self):
        """
        Test listing movies filtered by genre
        """
        serializer = MovieSerializer(self.genre.movies.all().order_by('name'), many=True)
        
        response = self.client.get(
            RESOURCE_URL, 
            {
                'genre': self.genre.id
            }
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'], serializer.data)
        
    def test_list_movies_filter_by_release_year(self):
        """
        Test listing movies filtered by release year
        """
        
        response = self.client.get(
            RESOURCE_URL, 
            {
                'release_year': '2000'
            }
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_list_movies_filter_by_name(self):
        """
        Test listing movies filtered by name
        """
        
        response = self.client.get(
            RESOURCE_URL, 
            {
                'name': 'Moovie'
            }
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class TestRetrieveMovie(APITestCase):
    def setUp(self):
        self.genre = sample_genre()
        self.movie = sample_movie(genre=self.genre)
    
    
    def test_retrieve_movie(self):
        """
        Test retrieving a movie
        """
        serializer = MovieSerializer(self.movie)
        
        response = self.client.get(
            detail_url(self.movie.id)
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        
    def test_retrieve_movie_not_found(self):
        """
        Test retrieving a movie not found
        """
        response = self.client.get(
            detail_url(999)
        )
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
