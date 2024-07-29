from django.db import models

class MoviesSearched(models.Model):
    title = models.CharField(max_length=200)
    released = models.CharField(max_length=100)
    runtime = models.CharField(max_length=50)
    imdb_rating = models.CharField(max_length=10)
    count = models.IntegerField(default=1)

    def __str__(self):
        return self.title
