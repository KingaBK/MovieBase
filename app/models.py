from django.db import models

# Create your models here.


class Movie(models.Model):
    movie_id = models.UUIDField(editable=False, unique=True)
    title = models.CharField(max_length=50, editable=False, unique=True)
    year = models.IntegerField()
    runtime = models.IntegerField()
    director = models.CharField(max_length=50)

    def __str__(self):
        return "Movie: title={}, year={}, runtime={} min, director={}".format(
            self.title, self.year, self.runtime, self.director)

    def get_absolute_url(self):
        """
        :return: url - access to created movie
        """
        return "/movies/{}/".format(self.title)


class Genre(models.Model):
    name = models.CharField(max_length=50, editable=False, unique=True)
    movies = models.ManyToManyField(Movie)

    def __str__(self):
        return "Movie genre: name={}".format(self.name)


class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    movies = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return "Movie genre: name={}".format(self.content)
