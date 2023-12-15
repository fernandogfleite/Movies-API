from api.apps.movies.models.movies import Genre
from api.apps.movies.serializers.movies import GenreSerializer

from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework import status

RESOURCE_URL = reverse('movies:genres-list')

def detail_url(genre_id):
    """
    Return genre detail URL
    """
    
    return reverse('movies:genres-detail', args=[genre_id])


def sample_genre(name='Test Genre'):
    """
    Create a sample genre
    """
    
    return Genre.objects.create(name=name)


class TestListGenres(APITestCase):
    def setUp(self):
        self.genre = sample_genre()
        sample_genre(name='Test Genre 2')
        sample_genre(name='Test Genre 3')
        
    def test_list_genres(self):
        """
        Test listing genres
        """
        
        response = self.client.get(RESOURCE_URL)
        
        genres = Genre.objects.all().order_by('name')
        serializer = GenreSerializer(genres, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)

        
    def test_list_genres_with_filter_by_name(self):
        """
        Test listing genres with filter by name
        """
        
        response = self.client.get(RESOURCE_URL, {'name': 'Test Genre 3'})
        
        genres = Genre.objects.filter(name='Test Genre 3').order_by('name')
        serializer = GenreSerializer(genres, many=True)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], serializer.data)
    

class TestRetrieveGenre(APITestCase):
    def setUp(self):
        self.genre = sample_genre()
        
    def test_retrieve_genre(self):
        """
        Test retrieving a genre
        """
        
        url = detail_url(self.genre.id)
        response = self.client.get(url)
        
        serializer = GenreSerializer(self.genre)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_retrieve_genre_not_found(self):
        """
        Test retrieving a genre that does not exist
        """
        
        url = detail_url(999)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
