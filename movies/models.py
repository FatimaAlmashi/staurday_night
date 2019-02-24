from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



class Genre(models.Model):
	title = models.CharField(max_length=50)

	def __str__(self):
		return self.title


class Movie(models.Model):
	title = models.CharField(max_length=50)
	added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movies')
	description = models.TextField()
	genres = models.ManyToManyField(Genre, related_name='movies')
	poster = models.ImageField(upload_to='movie_posters')
	release_date = models.DateField()

	class Meta:
		ordering = ['release_date', 'title']

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('movie-detail', kwargs={'movie_id': self.id})

	def update_url(self):
		return reverse('update-movie', kwargs={'movie_id': self.id})


class Favorite(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
	movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorites')

	def __str__(self):
		return "%s favorited %s"%(self.user.username, self.movie.title)

