import uuid
from typing import List

from rest_framework.request import Request
from rest_framework.utils import serializer_helpers
from rest_framework.exceptions import ValidationError

from app import models
from app.filters import MovieFilter, CommentFilter
from app.serializers import CommentSerializer, MovieSerializer


class MovieService:

    def create(self, request: Request) -> serializer_helpers.ReturnDict:
        valid_data = {
            "movie_id": uuid.uuid4(),
            "title": request.data["title"],
            "year": 2018,
            "runtime": 125,
            "director": "Jan Kowalski"
        }

        movie = models.Movie.objects.create(**valid_data)
        movie_data = MovieSerializer(movie).data

        return movie_data

    def get(self, request: Request) -> List[serializer_helpers.ReturnDict]:
        movie_filter = MovieFilter(request.query_params)
        if not movie_filter.is_valid():
            raise ValidationError("Query not valid.")

        movies_query = movie_filter.filter_queryset(models.Movie.objects.all())

        movies_list = []
        for movie in movies_query.order_by("title"):
            movies_list.append(MovieSerializer(movie).data)

        return movies_list


class CommentService:
    def create(self, request: Request) -> serializer_helpers.ReturnDict:
        movie = models.Movie.objects.get(movie_id=request.data["movie_id"])
        valid_data = {
            "content": request.data["content"],
            "movie": movie
        }

        comment = models.Comment.objects.create(**valid_data)
        comment_data = CommentSerializer(comment).data

        return comment_data

    def get(self, request: Request) -> List[serializer_helpers.ReturnDict]:
        comment_filter = CommentFilter(request.query_params)
        if not comment_filter.is_valid():
            raise ValidationError("Query not valid.")

        comments_query = comment_filter.filter_queryset(models.Comment.objects.all())

        comment_list = []
        for c_q in comments_query:
            comment_list.append(CommentSerializer(c_q).data)

        return comment_list
