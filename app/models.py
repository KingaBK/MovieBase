from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=50, editable=False, unique=True)

    def __str__(self):
        return "Movie genre: name={}".format(self.name)


class Movie(models.Model):
    movie_id = models.UUIDField(editable=False, unique=True)
    title = models.CharField(max_length=50, editable=False, unique=True)
    year = models.IntegerField()
    runtime = models.CharField(max_length=15)
    director = models.CharField(max_length=50)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return "Movie: title={}, year={}, runtime={}, director={}, genre={}".format(
            self.title, self.year, self.runtime, self.director, list(self.genre.all()))


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return "Movie comment: content={}".format(self.content)
