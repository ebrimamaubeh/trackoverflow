from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from taggit.managers import TaggableManager
from django.core.exceptions import ObjectDoesNotExist


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

def get_tags_string(post):
    tags = post.tags.all()
    res = ""
    for tag in tags: 
        res = res + tag.name

    return res.replace('"', ' ') # remove double quote 


def postQuestion(request):
    if request.method == 'POST':
        # hint: 
        # https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_many/
        form = PostForm(request.POST)
        #TODO: not working 
        if form.is_valid(): # make sure validation is working later, 
            if request.user.is_authenticated: 
                post = Post.objects.create(user=request.user, title=request.POST.get('title'), content=request.POST.get('content'))
                post.tags.add(request.POST.get('tags'))
                post.save()

                return redirect('post:index')
            else:
                messages.error(request, 'You must be logged in to post!')
                return render(request, 'post/question.html', context={'form': form})

        else:
            return error_status(400, 'invalid form values') # TODO: check errors/messaging

        return redirect('post:index')

    if request.method == 'GET': 
        form = PostForm()
        return render(request, 'post/question.html', context={'form': form})

def update_post(request): 
    try:
        post = Post.objects.get(id=int(request.POST.get('post_id')))
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        
        tags_string = request.POST.get('tags')

        post.tags.clear() # clear old tags
        post.tags.add(tags_string)
        post.save()

        return redirect('post:index')
    except ObjectDoesNotExist as e: 
        return HttpResponse('Post does not exist!', status=404) 

def update_post_view(request, post_id):
    try:
        post = Post.objects.get(id=post_id) 
        data = {'title': post.title, 'content': post.content, 'tags': get_tags_string(post)}
        post_form = PostForm(data)
        return render(request, "post/update_post_view.html", context={'post_form': post_form, 'post': post})
    except ObjectDoesNotExist as e:
        return HttpResponse('Post does not exist!', status=404)

    
def delete_post(request, post_id): 
    try: 
        Post.objects.get(id=post_id).delete()
        return redirect('post:index')
    except: 
        messages.error(request, 'The Post does not exist!') 
        return redirect('post:index')

