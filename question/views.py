from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .forms import QuestionForm, AnswerForm
from question.models import Answer, Question 


def index(request): 
	questions = Question.objects.all()
	return render(request, "question/index.html", context={'questions': questions})


#show post in detail.
def detail(request, question_id):
	try:
		question = get_object_or_404(Question, id=question_id)
		question.question_views += 1
		question.save()

		answer_form = AnswerForm()

		#getting answers of this question
		answers = Answer.objects.filter(user=question.user, question=question)

		context = {'question': question, 'answer_form': answer_form, 'answers': answers}
		return render(request, "question/detail.html", context=context)
	except Exception as e:
		raise e
		messages.error(request, "That post does not exist!")

	return redirect("question:detail")


#Todo: see prompt of delete. 
def delete_question(request, question_id):
	question = get_object_or_404(Question, id=question_id)
	question.delete()
	messages.success(request, "Question deleted!")

	return redirect("question:index")


@require_http_methods(['GET', 'POST'])
def edit_question(request, question_id):
	post = None

	try: 
		question = Question.objects.get(id=question_id)
	except Exception as e: 
		raise e

	if request.method == 'GET':
		tags = question.tags.all()
		tags_string = (''.join(str(e) +',' for e in tags))
		tags_string = tags_string[:-1] # remove the last ','
		c = {'question': question, 'tags_string': tags_string}

		return render(request, "question/edit.html", context=c)
	else: 
		#TODO; create form and check if valid.
		title = request.POST.get('title')
		content = request.POST.get('content')
		editForm = QuestionForm(request.POST)

		#add tags. 
		for t in request.POST.get('tags').split(','):
			question.tags.add(t.replace(",", ""))
		
		return redirect("question:detail", post_id=post_id)


@require_http_methods(['GET', 'POST'])
def ask_question(request):
	if request.method == 'GET':
		form = QuestionForm()
		return render(request, 'question/new_question.html', context={'form': form})
	elif request.method == 'POST': 
		tags = request.POST.get('tags')
		form = QuestionForm(request.POST)
		
		if request.user.is_authenticated:
			if form.is_valid():
				question = form.save(commit=False) # created, not saved
				
				# proccess question, here...
				question.user = request.user
				question.save() # Finally save post in db.

				for t in tags.split():
					question.tags.add(t.replace(",", ""))

				question.save()

				messages.success(request, "Question post successfuly created!")
				return redirect("question:detail", question_id=question.id)
			else: 
				messages.error(request, 'invalid form values')
				return render(request, 'question/new_question.html', context={'form': form})
		else: 
			# TODO: Just redirect them to the login page. 
			messages.error(request, 'You must be logged in to post!')
			return render(request, 'question/new_question.html', context={'form': form})

def tags_list(request, tag):
	questions = Question.objects.filter(tags__name__in=[tag])
	return render(request, "question/tags_list.html", context={'questions': questions})


@require_http_methods(['POST'])
def answer_question(request, question_id):
	question = get_object_or_404(Question, id=question_id)
	question.number_of_answers += 1
	question.save()

	answer = Answer()
	answer.user = request.user 
	answer.question = question 
	answer.content = request.POST.get('content')
	answer.save()

	messages.success(request, "Answer to Question posted!")
	return redirect('question:detail', question_id=question.id)


def delete_answer(request, question_id, answer_id):
	answer = get_object_or_404(Answer, id=answer_id)
	answer.delete()
	messages.success(request, "Answer successfuly deleted")
	return redirect("question:detail", question_id=question_id)


