from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
	title = models.CharField(max_length=128)
	description = models.CharField(max_length=256)
	created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='movies')

	def __str__(self):
		return self.title