from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    BranchPostListView,
    YearPostListView,
    CommentFormView,
    CommentUpdateView
)
from django.views.decorators.http import require_POST
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/blog/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('blog/<str:branch>', BranchPostListView.as_view(), name='branch-posts'),
    path('blog/<str:branch>/<str:year_of_admission>', YearPostListView.as_view(), name='year-posts'),
    url('like/',views.like , name='like'),
    url('just_parent/',views.just_parent , name='just-parent'),
    path('comment_form/<str:pkey>/',require_POST(CommentFormView.as_view()),name='comment-form'),
    path('comment_update/<str:pkey>/<int:pk>/',require_POST(CommentUpdateView.as_view()),name='comment-update'),
]

#url('like/',views.like , name='like'),
