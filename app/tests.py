import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from app import models


class MoviesPostTests(APITestCase):

    @patch('app.omdb_api.fetch_movie_details')
    def test_creating_movie(self, fetch_movie_details_mock):
        """
        Ensure we can create a new movie object.
        """
        # Given
        return_text = json.dumps({
            "Title": "Shrek",
            "Year": 2000,
            "Runtime": "125 min",
            "Genre": "Comedy, Family",
            "Director": "A. B.",
            "Response": "True"
        })
        fetch_movie_details_mock.return_value = (200, return_text, None)
        url = reverse('movies')
        data = {'title': 'Shrek'}

        # When
        response = self.client.post(url, data)

        # Then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(models.Movie.objects.count(), 1)
        self.assertEqual(models.Movie.objects.get().title, 'Shrek')
        self.assertTrue(fetch_movie_details_mock.called)

    @patch('app.omdb_api.fetch_movie_details')
    def test_not_creating_duplicate_movie(self, fetch_movie_details_mock):
        """
        Ensure we cannot create the same movie object twice.
        """
        # Given
        return_text = json.dumps({
            "Title": "Pocahontas",
            "Year": 1999,
            "Runtime": "110 min",
            "Genre": "Comedy, Family, Romance",
            "Director": "C. D.",
            "Response": "True"
        })
        fetch_movie_details_mock.return_value = (200, return_text, None)
        url = reverse('movies')
        data = {'title': 'Pocahontas'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # When
        response2 = self.client.post(url, data)

        # Then
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(models.Movie.objects.count(), 1)

    @patch('app.omdb_api.fetch_movie_details')
    def test_received_response_data(self, fetch_movie_details_mock):
        """
        Ensure sent data have all required fields.
        """
        # Given
        return_text = json.dumps({
            "Title": "Pocahontas",
            "Year": 1999,
            "Runtime": "110 min",
            "Genre": "Comedy, Family, Romance",
            "Director": "C. D.",
            "Response": "True"
        })
        fetch_movie_details_mock.return_value = (200, return_text, None)
        url = reverse('movies')
        data = {'title': 'Pocahontas'}

        # When
        response = self.client.post(url, data)

        # Then
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("title", response.data)
        self.assertIn("movie_id", response.data)
        self.assertIn("year", response.data)
        self.assertIn("runtime", response.data)
        self.assertIn("director", response.data)


class MoviesGetTests(APITestCase):

    @patch('app.omdb_api.fetch_movie_details')
    def _load_movies(self, fetch_movie_details_mock):
        url = reverse('movies')
        movies = {
            "Shrek": {
                "Title": "Shrek",
                "Year": 2000,
                "Runtime": "125 min",
                "Genre": "Comedy, Family",
                "Director": "A. B.",
                "Response": "True"
            },
            "Pocahontas": {
                "Title": "Pocahontas",
                "Year": 1999,
                "Runtime": "110 min",
                "Genre": "Comedy, Family, Romance",
                "Director": "C. D.",
                "Response": "True"
            },
            "Joker": {
                "Title": "Joker",
                "Year": 2019,
                "Runtime": "160 min",
                "Genre": "Comedy, Thriller, Drama",
                "Director": "E. F.",
                "Response": "True"
            },

        }
        for title, details in movies.items():
            return_text = json.dumps(details)
            fetch_movie_details_mock.return_value = (200, return_text, None)
            data = {'title': title}
            self.client.post(url, data)

    def test_getting_empty_movies(self):
        """
        Ensure response contains empty list, when no movies in database.
        """
        # Given
        url = reverse('movies')

        # When
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_getting_all_movies(self):
        """
        Ensure response contains all movies.
        """
        # Given
        self._load_movies()
        url = reverse('movies')

        # When
        response = self.client.get(url)
        titles = []
        for movie_details in response.data:
            titles.append(movie_details["title"])

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Shrek', titles)
        self.assertIn('Pocahontas', titles)
        self.assertIn('Joker', titles)

    def test_getting_sorted_movies(self):
        """
        Ensure response contains movies sorted by title.
        """
        # Given
        url = reverse('movies')
        self._load_movies()

        # When
        response = self.client.get(url)
        titles = []
        for movie_details in response.data:
            titles.append(movie_details["title"])

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(titles, ['Joker', 'Pocahontas', 'Shrek'])

    def test_getting_filtered_movies(self):
        """
        Ensure response contains movies filtered by genre (genre must include Family).
        """
        # Given
        self._load_movies()
        url = "{}?genre={}".format(reverse('movies'), 'Family')

        # When
        response = self.client.get(url)
        titles = []
        for movie_details in response.data:
            titles.append(movie_details["title"])

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(titles, ['Pocahontas', 'Shrek'])
