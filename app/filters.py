from django_filters import FilterSet
from app import models


class MovieFilter(FilterSet):

    class Meta:
        model = models.Movie
        fields = ["year", "runtime", "director"]


class CommentFilter(FilterSet):

    class Meta:
        model = models.Comment
        fields = ["movie__movie_id"]
