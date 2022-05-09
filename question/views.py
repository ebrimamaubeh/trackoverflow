from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .forms import QuestionForm, AnswerForm
from question.models import Answer, Question, QuestionComment, AnswerComment

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError


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

		questionComments = QuestionComment.objects.filter(question=question)

		context = {
			'question': question, 'answer_form': answer_form, 
			'answers': answers, 'questionComments': questionComments
		}
		return render(request, "question/detail.html", context=context)
	except Exception as e:
		raise e
		messages.error(request, "That post does not exist!")
		return redirect("question:detail")


#Todo: see prompt of delete. 
@login_required
def delete_question(request, question_id):
	question = get_object_or_404(Question, id=question_id)
	if request.user != question.user: 
		raise PermissionDenied("you can only delete questions you asked!")
	
	question.delete()
	messages.success(request, "Question deleted!")

	return redirect("question:index")

#TODO: question edit not working
@require_http_methods(['GET', 'POST'])
@login_required
def edit_question(request, question_id):
	question = get_object_or_404(Question, id=question_id)

	if request.method == 'GET':
		tags = question.tags.all()
		tags_string = (''.join(str(e) +',' for e in tags))
		tags_string = tags_string[:-1] # remove the last ','
		c = {'question': question, 'tags_string': tags_string}

		return render(request, "question/edit.html", context=c)
	else: 
		title = request.POST.get('title')
		content = request.POST.get('content')

		#TODO; validate data.
		has_errors = False 
		if len(title) < 5:
			has_errors = True 
			messages.error(request, 'Ttile must be more than 5 characters!')
		if len(content) < 10: 
			has_errors = True
			messages.error(request, 'Content must be more than 10 characters!')

		if has_errors: 
			return 
		#TODO; validate data.

		question.title = title
		question.content = content

		#add tags. 
		for t in request.POST.get('tags').split(','):
			question.tags.add(t.replace(",", ""))

		question.save()
		
		return redirect("question:detail", question_id=question_id)


@require_http_methods(['GET', 'POST'])
@login_required
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
@login_required
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


@require_http_methods(['POST'])
@login_required
def question_comment(request, question_id):
	question = get_object_or_404(Question, id=question_id)
	content = request.POST.get('content')
	if not content:
		raise ValueError("Comment message is required!")

	comment = QuestionComment(content=content)
	comment.question = question
	comment.content = content
	comment.user = request.user
	comment.save()

	return redirect('question:detail', question_id=question_id)

@require_http_methods(['POST'])
@login_required
def answer_comment(request, question_id, answer_id):
	answer = get_object_or_404(Answer, id=answer_id)
	content = request.POST.get('content')
	if not content: 
		raise ValueError("Message of the comment required!")
	comment = AnswerComment(content=content)
	comment.answer = answer
	comment.user = request.user 
	comment.save()

	return redirect('question:detail', question_id=question_id)


@require_http_methods(['GET'])
@login_required
def delete_question_comment(request, question_id, comment_id):
	comment = get_object_or_404(QuestionComment, id=comment_id)
	if request.user != comment.user: 
		raise PermissionDenied("you can only delete questions you asked!")

	comment.delete()
	messages.success(request, "Comment successfuly deleted")
	return redirect("question:detail", question_id=question_id)

def delete_answer_comment(request, question_id, answer_comment_id): 
	answerComment = get_object_or_404(AnswerComment, id=answer_comment_id)
	if request.user != answerComment.user: 
		raise PermissionDenied("you can only delete questions you asked!")

	answerComment.delete()
	messages.success(request, "Comment successfuly deleted")
	#check how you can redirect on specific section of the page.
	return redirect("question:detail", question_id=question_id)

@require_http_methods(['POST'])
@login_required
def edit_question_comment(request, question_id, comment_id): 
	questionComment = get_object_or_404(QuestionComment, id=comment_id)
	if request.user != questionComment.user: 
		raise PermissionDenied("you can only edit what you written!")

	content = request.POST.get('content')
	if len(content) < 10: 
		raise ValueError('content must be greate than 10 characters')

	questionComment.content = content
	questionComment.save()

	return redirect("question:detail", question_id=question_id)

@require_http_methods(['GET'])
@login_required
def get_question_comment(request, comment_id):
	questionComment = get_object_or_404(QuestionComment, id=comment_id)
	if request.user != questionComment.user: 
		raise PermissionDenied("you can only edit what you written!")

	return HttpResponse(questionComment.content)