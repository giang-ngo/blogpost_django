from django.urls import path
from .import views

urlpatterns = [
    path('', views.posts, name='posts'),
    path('post/<str:pk>/', views.postDetail, name='post_detail'),
    path('post_create/', views.postCreate, name='post_create'),
    path('post_update/<str:pk>/', views.postUpdate, name='post_update'),
    path('post_delete/<str:pk>/', views.postDelete, name='post_delete'),
    path('message_delete/<str:pk>/', views.messageDelete, name='message_delete'),
    path('admin_delete/<str:pk>/', views.adminDelete, name='admin_delete'),
    path('post_like/<str:pk>/', views.postLike, name='post_like'),
    path('create_comment/<str:pk>/', views.createComment, name='create_comment'),
    path('reply_comment/<post_id>/<message_id>/',
         views.replyComment, name='reply_comment'),

    path('admin_approval/', views.adminApproval, name='admin_approval'),

]
