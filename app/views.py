from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request

# Create your views here.


class MovieCollection(APIView):
    def post(self, request: Request, format=None):
        pass

    def get(self, request: Request, format=None):
        pass


class CommentCollection(APIView):
    def post(self, request: Request, format=None):
        pass

    def get(self, request: Request, format=None):
        pass


class TopResource(APIView):
    def get(self, request: Request, format=None):
        pass
