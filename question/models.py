from django.db import models

from post.models import Post 

# Create your models here.
class Question(models.Model):
	post = models.ForeignKey(Post, on_delete=models.PROTECT)
	