from django import forms 
from django.db import models
from django.forms import ModelForm
from .models import Post


class PostForm(ModelForm): 
    class Meta: 
        model = Post
        fields = ['title', 'content', 'tags']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs.update({
            'class': 'u-border-1 u-border-grey-30 u-input u-input-rectangle u-white', 
            'placeholder': "A comma separated list of tags"

            })
    