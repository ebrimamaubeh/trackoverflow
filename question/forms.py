from django.forms import ModelForm
from django import forms 

from .models import Answer, Question

class QuestionForm(ModelForm): 
	class Meta: 
		model = Question
		fields = ['title', 'content', 'tags']

	#validation function
	def clean(self):
		super(QuestionForm, self).clean()

		#extract data from form. 
		title = self.cleaned_data.get('title')
		content = self.cleaned_data.get('content')
		tags = self.cleaned_data.get('tags')

		#validation conditinos. 
		if len(title) < 5: 
			self._errors['title'] = self.error_class(
				['Title must have a minimum of 5 characters']
			)
		if len(content) < 10: 
			self._errors['content'] = self.error_class(
				['content must be at least 10 characters']
			)

		return self.cleaned_data

class AnswerForm(ModelForm):
	class Meta: 
		model = Answer
		fields = ['content']

	def clean(self):
		super(AnswerForm, self).clean()

		content = self.cleaned_data.get('content')
		if len(content) == 0: 
			self._errors['content'] = self.error_class(
				['The Answer field is required.']
			)

		return self.cleaned_data