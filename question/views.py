from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages

from post.models import Post
from .forms import PostForm, AnswerForm
from question.models import Answer, Question 


def index(request): 
	posts = Post.objects.all()
	return render(request, "question/index.html", context={'posts': posts})


#show post in detail.
def detail(request, post_id):
	try:
		post = Post.objects.get(id=post_id)
		post.post_views += 1
		post.save()

		form = AnswerForm()

		#getting answers of this question
		# question = Question.objects.get(user=request.user, post=post)
		# answers = Answer.objects.get(user=request.user, question=q)


		context = {'post': post, 'form': form}
		return render(request, "question/detail.html", context=context)
	except Exception as e:
		raise e
		messages.error(request, "That post does not exist!")

	return redirect("question:index")


#Todo: see prompt of delete. 
def delete_post(request, post_id):
	try:
		post = Post.objects.get(id=post_id)
		post.delete()
		messages.success(request, "Post deleted!")
	except Exception as e:
		messages.error(request, "Post does not exist for delete")
		raise e 

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

				# create and save question. 
				Question.objects.create(user=request.user, post=post)

				# load the detailed post of the created post. 
				messages.success(request, "Question post successfuly created!")
				return redirect("question:detail", post_id=post.id)
			else: 
				messages.error(request, 'invalid form values')
				return render(request, 'question/new_question.html', context={'form': form})
		else: 
			# TODO: Just redirect them to the login page. 
			messages.error(request, 'You must be logged in to post!')
			return render(request, 'question/new_question.html', context={'form': form})

def tags_list(request, tag):
	posts = Post.objects.filter(tags__name__in=[tag])
	return render(request, "question/tags_list.html", context={'posts': posts})


@require_http_methods(['POST'])
def answer_question(request, post_id):
	try:
		post = Post.objects.get(id=post_id)
		question = Question(user=request.user, post=post)
		question.save()

		answer = Answer()
		answer.user = request.user 
		answer.question = question 
		answer.content = request.POST.get('content')
		answer.save()

		messages.success(request, "Answer to Question posted!")
		return redirect('question:detail', post_id=post_id)

	except Exception as e:
		raise e
		messages.error(request, "The question you are trying to answer does not exist!")
		return redirect("question:index")

