from django.urls import path

from . import views 

app_name = 'post'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:post_id>/', views.detail, name='detail_post'),
    path('ask/', views.postQuestion, name='post_question'), 
    path('update/post/', views.update_post, name='update_post'), 
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'), 
    path('update/view/<int:post_id>/', views.update_post_view, name='update_post_view'),
    path('like/<int:post_id>/', views.likePost, name='likePost'),
]
