from django.db import models
from django.contrib.auth.models import User 

#method to help with user is created/updated, profile will be called. 
from django.db.models.signals import post_save
from django.dispatch import receiver 

# Create your models here.

class Profile(models.Model):
    #TODO: continue where the profile form is created (one to one relationships)
    #TODO: source: https://simpleisbetterthancomplex.com/tutorial/2016/07/22/how-to-extend-django-user-model.html
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    biography = models.TextField(max_length=150, blank=True)
    location = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_pic = models.CharField(max_length=50, default='static/img/default.png')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def _post_save_receiver(sender, instance, **kwargs):
    instance.profile.save()

    

