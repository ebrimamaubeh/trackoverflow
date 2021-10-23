from django.db import models
from post.models import Post 

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.PROTECT)
    content = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)