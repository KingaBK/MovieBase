from django.db import models


class Movie(models.Model):
    movie_id = models.UUIDField(editable=False, unique=True)
    title = models.CharField(max_length=50, editable=False, unique=True)
    year = models.IntegerField()
    runtime = models.IntegerField()
    director = models.CharField(max_length=50)

    def __str__(self):
        return "Movie: title={}, year={}, runtime={} min, director={}".format(
            self.title, self.year, self.runtime, self.director)


class Genre(models.Model):
    name = models.CharField(max_length=50, editable=False, unique=True)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return "Movie genre: name={}".format(self.name)


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return "Movie comment: content={}".format(self.content)
