from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


# https://django-taggit.readthedocs.io/en/latest/api.html
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=50)
    content = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    number_of_answers = models.IntegerField(default=0)
    tags = TaggableManager()
    