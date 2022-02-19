from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404


# def post_comment(request): 
#     try:
#         post_id = int(request.POST.get('post_id'))
#         post = Post.objects.get(id=post_id)
#         content = request.POST.get('post_comment_content')
#         comment = Comment.objects.create(post=post, content=content)
#         comment.save()
#         return redirect('post:detail_post', post_id=post_id)
#     except Post.DoesNotExist as e:
#         return Http404('The post you are trying to comment on does not exist!')
