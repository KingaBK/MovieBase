import uuid
from rest_framework import serializers

from app import models


class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Movie
        exclude = ("id",)


class CommentSerializer(serializers.ModelSerializer):
    movie_id = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = ["content", "movie_id", "created_at"]

    def get_movie_id(self, obj) -> uuid.UUID:
        return obj.movie.movie_id
