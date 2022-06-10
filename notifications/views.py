from django.shortcuts import render
from django.contrib.auth.models import User
from notifications.models import Notification
from question.models import Question, Answer
from django.shortcuts import get_object_or_404


def track_question_notification(request, question_id):
	question = get_object_or_404(Question, id=question_id)
	# nt = NotificationTracker()
	# nt.user = request.user 
	# nt.question = question
	# nt.save()

	return HttpResponse("This question will be tracked!")

def track_answer_notification(request, answer_id):
	answer = get_object_or_404(Answer, id=answer_id)
	# nt = NotificationTracker()
	# nt.user = request.user 
	# nt.answer = answer
	# nt.save()

	return HttpResponse("This answer will be tracked!")

