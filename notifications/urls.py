from django.urls import path

from . import views 

app_name = 'notifications'
urlpatterns = [
    #js functions
    path('register/question/<int:question_id>/', views.track_question_notification),
    path('register/answer/<int:answer_id>/', views.track_answer_notification),
]   
