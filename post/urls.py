from django.urls import path

from . import views 

app_name = 'post'
urlpatterns = [
    path('', views.index, name='index'),
    path('ask/', views.postQuestion, name='post_question')
]