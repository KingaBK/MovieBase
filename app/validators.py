from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
import uuid

from app import models


class MoviePostValidator:
    def __call__(self, request: Request):
        if "title" not in request.data:
            raise ValidationError("Title not given.")

        movie = models.Movie.objects.filter(title=request.data["title"])
        if movie:
            raise ValidationError("Title already exists.")


class MovieGetValidator:
    def __call__(self, request: Request):
        for q in request.query_params:
            if q not in ["year", "runtime", "director", "genre"]:
                raise ValidationError("Field {} not allowed in query.".format(q))


class CommentPostValidator:
    def __call__(self, request: Request):
        if "movie_id" not in request.data:
            raise ValidationError("Movie_id not given.")
        if "content" not in request.data:
            raise ValidationError("Content not given.")

        movie_id = request.data["movie_id"]

        try:
            uuid.UUID(hex=str(movie_id))
        except ValueError:
            raise ValidationError("Incorrect format of movie_id.")

        try:
            models.Movie.objects.get(movie_id=movie_id)
        except models.Movie.DoesNotExist:
            raise ValidationError("movie_id does not exist.")


class CommentGetValidator:
    def __call__(self, request: Request):
        for q in request.query_params:
            if q not in ["movie__movie_id"]:
                raise ValidationError("Field {} not allowed in query.".format(q))

        if "movie__movie_id" in request.query_params:
            movie_id = request.query_params["movie__movie_id"]

            try:
                uuid.UUID(hex=str(movie_id))
            except ValueError:
                raise ValidationError("Incorrect format of movie__movie_id.")


class TopGetValidator:
    def __call__(self, request: Request):
        for q in request.query_params:
            if q not in ["start_date", "end_date"]:
                raise ValidationError("Field {} not allowed in query.".format(q))
