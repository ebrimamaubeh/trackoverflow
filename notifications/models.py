from django.db import models
from django.contrib.auth.models import User
from question.models import Question
from question.models import Answer

from django.core.signals import request_finished
from django.dispatch import receiver

# Create your models here.
class Notification(models.Model):
	user = models.ForeignKey(User, on_delete=models.PROTECT)
	title = models.CharField(max_length=100)
	content = models.TextField()
	has_read = models.BooleanField(default=False)
	date_created = models.DateField(auto_now_add=True)



#signal functions. 
# from django.core.signals import request_finished
# from django.dispatch import reciever
# @reciever(request_finished,sender=User)

#this should be called when a question/answer is registered for notifications. 
#reciever should be in views. 
def create_notification(sender, **kwargs):
	pass

def check_user_notification():
	pass 
