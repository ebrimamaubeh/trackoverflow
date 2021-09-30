from django import forms 
from django.db import models
from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm): 
    class Meta: 
        model = Post
        fields = ['title', 'content', 'tags']