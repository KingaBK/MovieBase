from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from app import models
from app.validators import MoviePostValidator, CommentPostValidator, CommentGetValidator, TopGetValidator, \
    MovieGetValidator
from app.services import MovieService, CommentService


class MovieCollection(APIView):
    def post(self, request: Request, format=None):
        MoviePostValidator()(request)
        movie_data = MovieService().create(request)

        return Response(status=status.HTTP_201_CREATED, data=movie_data)

    def get(self, request: Request, format=None):
        MovieGetValidator()(request)
        movie_list = MovieService().get(request)

        return Response(status=status.HTTP_200_OK, data=movie_list)


class CommentCollection(APIView):
    def post(self, request: Request, format=None):
        CommentPostValidator()(request)
        comment_data = CommentService().create(request)

        return Response(status=status.HTTP_201_CREATED, data=comment_data)

    def get(self, request: Request, format=None):
        CommentGetValidator()(request)
        comment_list = CommentService().get(request)

        return Response(status=status.HTTP_200_OK, data=comment_list)


class TopResource(APIView):
    def get(self, request: Request, format=None):
        TopGetValidator()(request)
