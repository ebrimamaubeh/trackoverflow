from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
class Question(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	title = models.CharField(max_length=50)
	content = models.TextField()
	date_created = models.DateField(auto_now_add=True)
	last_updated = models.DateField(auto_now=True)
	number_of_answers = models.IntegerField(default=0)
	tags = TaggableManager()
	up_votes = models.IntegerField(default=0)
	down_votes = models.IntegerField(default=0)
	question_views = models.IntegerField(default=0)
	is_deleted = models.BooleanField(default=False)
	notify = models.BooleanField(default=False)

class Answer(models.Model):
	user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
	question = models.ForeignKey(Question, default=None, on_delete=models.PROTECT)
	content = models.TextField(null=True)
	up_votes = models.IntegerField(default=0)
	down_votes = models.IntegerField(default=0)
	is_deleted = models.BooleanField(default=False)
	notify = models.BooleanField(default=False)

class QuestionComment(models.Model):
	user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
	question = models.ForeignKey(Question, on_delete=models.PROTECT, default=None)
	content = models.TextField()
	date_created = models.DateField(auto_now_add=True)
	last_updated = models.DateField(auto_now=True)
	flag = models.BooleanField(default=False)
	up_votes = models.IntegerField(default=0)
	is_deleted = models.BooleanField(default=False)

class AnswerComment(models.Model):
	user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
	answer = models.ForeignKey(Answer, on_delete=models.PROTECT, default=None)
	content = models.TextField()
	date_created = models.DateField(auto_now_add=True)
	last_updated = models.DateField(auto_now=True)
	flag = models.BooleanField(default=False)
	up_votes = models.IntegerField(default=0)
	is_deleted = models.BooleanField(default=False)
	is_deleted = models.BooleanField(default=False)



#testing notifications. 
#functions i want to be called. 
# 1. users should indicate which questions/answers should be tracked. 


