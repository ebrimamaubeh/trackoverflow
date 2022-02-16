from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from post.models import Post
from .forms import PostForm


def index(request): 
	posts = Post.objects.all()
	return render(request, "question/index.html", context={'posts': posts})

def detail(request, post_id):
	try:
		post = Post.objects.get(id=post_id)
		post.post_views += 1
		post.save()
		return render(request, "question/detail.html", context={'post': post})
	except Exception as e:
		print(e)
		messages.error(request, "That post does not exist!")

	return redirect("question:index")

#Todo: see prompt of delete. 
def delete_post(request, post_id):
	try:
		post = Post.objects.get(id=post_id)
		post.delete()
	except Exception as e:
		print(e)
		messages.error(request, "Post does not exist for delete")

	return redirect("question:index")


@require_http_methods(['GET', 'POST'])
def edit_post(request, post_id):
	post = None

	try: 
		post = Post.objects.get(id=post_id)
	except Exception as e: 
		print(e)
		messages.error(request, "There is an error with the post edit!")
		return redirect("question:index")

	if request.method == 'GET':
		tags = post.tags.all()
		tags_string = (''.join(str(e) +',' for e in tags))
		tags_string = tags_string[:-1] # remove the last ','
		c = {'post': post, 'tags_string': tags_string}

		return render(request, "question/edit.html", context=c)
	else: 
		#TODO; create form and check if valid.
		title = request.POST.get('title')
		content = request.POST.get('content')
		editForm = PostForm(request.POST)

		#add tags. 
		for t in request.POST.get('tags').split(','):
			post.tags.add(t.replace(",", ""))
		
		return redirect("question:detail", post_id=post_id)


@require_http_methods(['GET', 'POST'])
def ask_question(request):
	if request.method == 'GET':
		form = PostForm()
		return render(request, 'question/new_question.html', context={'form': form})
	elif request.method == 'POST': 
		tags = request.POST.get('tags')
		form = PostForm(request.POST)
		
		if request.user.is_authenticated:
			if form.is_valid():
				post = form.save(commit=False) # post created, not saved
				
				# proccess post, here...
				post.user = request.user
				post.save() # Finally save post in db.

				for t in tags.split():
					post.tags.add(t.replace(",", ""))

				post.save()

				# load the detailed post of the created post. 
				return redirect("question:detail", post_id=post.id)
			else: 
				messages.error(request, 'invalid form values')
				return render(request, 'question/new_question.html', context={'form': form})
		else: 
			# TODO: Just redirect them to the login page. 
			messages.error(request, 'You must be logged in to post!')
			return render(request, 'question/new_question.html', context={'form': form})
