from django.shortcuts import render
from django.http import HttpResponse

from models import Question

def index(requests):
    # this function should return a list of all post. 
    questions = Question.objects.all()
    return render(requests, contex=questions)
