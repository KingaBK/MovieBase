from django_filters import FilterSet, filters, CharFilter
from app import models


class MovieFilter(FilterSet):
    genre = CharFilter(field_name='genre__name', lookup_expr='contains')

    class Meta:
        model = models.Movie
        fields = ["year", "runtime", "director", "genre"]


class CommentFilter(FilterSet):
    start_date = filters.IsoDateTimeFilter(field_name="created_at", lookup_expr='gte')
    end_date = filters.IsoDateTimeFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = models.Comment
        fields = ["movie__movie_id", "start_date", "end_date"]
