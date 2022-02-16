from django.urls import path

from . import views 

app_name = 'question'
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:post_id>/', views.detail, name='detail'),
    path('ask/', views.ask_question, name='ask_question'), 
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'), 
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'), 
    # path('update/view/<int:post_id>/', views.update_post_view, name='update_post_view'),
    # path('like/<int:post_id>/', views.likePost, name='likePost'),
    # path('test/', views.test, name="test"), 
]
