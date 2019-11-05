import uuid
from rest_framework import serializers

from app import models


class MovieSerializer(serializers.ModelSerializer):
    genre = serializers.SerializerMethodField()

    class Meta:
        model = models.Movie
        fields = ('movie_id', 'title', 'year', 'runtime', 'director', 'genre')

    def get_genre(self, obj):
        genre_names = []
        for g in obj.genre.all():
            genre_names.append(g.name)

        return ", ".join(genre_names)


class CommentSerializer(serializers.ModelSerializer):
    movie_id = serializers.SerializerMethodField()

    class Meta:
        model = models.Comment
        fields = ["content", "movie_id", "created_at"]

    def get_movie_id(self, obj) -> uuid.UUID:
        return obj.movie.movie_id
