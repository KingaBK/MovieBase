import json
import uuid
from typing import List, Dict

import requests
from rest_framework.request import Request
from rest_framework.utils import serializer_helpers
from rest_framework.exceptions import ValidationError

from app import models
from app.custom_exceptions import FailedDependencyError
from app.filters import MovieFilter, CommentFilter
import app.omdb_api as omdb_api
from app.serializers import CommentSerializer, MovieSerializer


class MovieService:

    def create(self, request: Request) -> Dict:
        all_details = self._fetch_movie_details(request.data["title"])

        valid_data = {
            "movie_id": uuid.uuid4(),
            "title": request.data["title"],
            "year": int(all_details["Year"]),
            "runtime": all_details["Runtime"],
            "director": all_details["Director"]
        }

        movie = models.Movie.objects.create(**valid_data)

        for g in all_details["Genre"].split(","):
            genre, created = models.Genre.objects.get_or_create(name=g.strip())
            movie.genre.add(genre)

        movie_data = MovieSerializer(movie).data

        return movie_data

    def get(self, request: Request) -> List[serializer_helpers.ReturnDict]:
        movie_filter = MovieFilter(request.query_params)
        if not movie_filter.is_valid():
            raise ValidationError("Query not valid. Errors={}".format(movie_filter.errors))

        movies_query = movie_filter.filter_queryset(models.Movie.objects.all())

        movies_list = []
        for movie in movies_query.order_by("title"):
            movies_list.append(MovieSerializer(movie).data)

        return movies_list

    def _fetch_movie_details(self, title) -> Dict:
        status_code, page_text, reason = omdb_api.fetch_movie_details(title)

        if status_code != 200:
            raise FailedDependencyError("Error at fetching movie details. Code={}, reason={}".format(status_code, reason))

        all_details = json.loads(page_text)
        if all_details["Response"] == "False":
            raise ValidationError({"Error": all_details["Error"]})

        return all_details


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
            raise ValidationError("Query not valid. Errors={}".format(comment_filter.errors))

        comments_query = comment_filter.filter_queryset(models.Comment.objects.all())

        comment_list = []
        for c_q in comments_query:
            comment_list.append(CommentSerializer(c_q).data)

        return comment_list


class TopService:
    def get(self, request: Request):
        comment_filter = CommentFilter(request.query_params)
        if not comment_filter.is_valid():
            raise ValidationError("Query not valid. Errors={}".format(comment_filter.errors))

        statistics = []
        for movie in models.Movie.objects.all():
            movie_comments = movie.comment_set.all()
            comment_query = comment_filter.filter_queryset(movie_comments)
            statistics.append(
                {
                    "movie_id": movie.movie_id,
                    "total_comments": comment_query.count()
                }
            )

        statistics.sort(key=lambda el: el["total_comments"], reverse=True)
        self._add_rank(statistics)

        return statistics

    def _add_rank(self, statistics: List[Dict]) -> None:
        rank = 1
        comments_count = statistics[0]["total_comments"]
        for i, el in enumerate(statistics):
            if el["total_comments"] < comments_count:
                comments_count = el["total_comments"]
                rank += 1
            el["rank"] = rank
