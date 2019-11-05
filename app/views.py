from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from app.custom_exceptions import FailedDependencyError
from app.validators import MoviePostValidator, CommentPostValidator, CommentGetValidator, TopGetValidator, \
    MovieGetValidator
from app.services import MovieService, CommentService, TopService


class MovieCollection(APIView):
    def post(self, request: Request, format=None):
        MoviePostValidator()(request)
        try:
            movie_data = MovieService().create(request)
        except FailedDependencyError as e:
            return Response(status=status.HTTP_424_FAILED_DEPENDENCY, data={"Error": str(e)})

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
        rank_list = TopService().get(request)

        return Response(status=status.HTTP_200_OK, data=rank_list)
