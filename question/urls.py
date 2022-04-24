from django.urls import path

from . import views 

app_name = 'question'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:question_id>/', views.detail, name='detail'),
    path('ask/', views.ask_question, name='ask_question'), 
    path('delete/<int:question_id>/', views.delete_question, name='delete_question'), 
    path('edit/<int:question_id>/', views.edit_question, name='edit_question'), 
    path('tags/<slug:tag>', views.tags_list, name="tags_list"), 
    path('answer/<int:question_id>/', views.answer_question, name="answer_question"),
    path('answer/delete/<int:question_id>/<int:answer_id>/', views.delete_answer, name="delete_answer"),
    path('comment/new/<int:question_id>/', views.question_comment, name='question_comment'),
    path('answer/comment/new/<int:question_id>/<int:answer_id>/', views.answer_comment, name='answer_comment'),
]
