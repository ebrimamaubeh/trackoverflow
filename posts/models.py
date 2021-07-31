from django.db import models
from tags import Tag 

# Create your models here.
class Question(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    date_created = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE, default=None)
    number_of_answers = models.IntegerField()
    