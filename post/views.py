from django.shortcuts import render, redirect
from django.http import HttpResponse


from post.models import Post
from .forms import PostForm 

def index(request):
    posts = Post.objects.all()
    return render(request, 'post/index.html' ,context={'posts': posts})


def error_status(status, reason=None):
    if reason is None:
        return HttpResponse(status=status)
    else:
        return HttpResponse(status=status, reason=reason)

def postQuestion(request):
    if request.method == 'POST':
        # hint: 
        # https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_many/
        form = PostForm(request.POST)
        if form.is_valid(): # make sure validation is working later, 
            form.save()
        else:
            return error_status(400, 'invalid form values') # TODO: check errors/messaging

        return redirect('post:index')

    if request.method == 'GET': 
        form = PostForm()
        return render(request, 'post/question.html', context={'form': form})
