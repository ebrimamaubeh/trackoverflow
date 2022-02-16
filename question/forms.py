from django.forms import ModelForm
from django import forms 

from post.models import Post 

class PostForm(ModelForm): 
	class Meta: 
		model = Post
		#custom fields. 
		fields = ['title', 'content', 'tags']

	#validation function
	def clean(self):
		# get form data. 
		super(PostForm, self).clean()

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