from django.urls import path
from blog.views.post_view import BlogLikeDislikeView, PostListView, PostDetailView, PostCreateView
from blog.views.comment_view import CommentListCreateView, \
    CommentDetailView

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post_list'),
    path('posts/create', PostCreateView.as_view(), name='post_create'),
    path('posts/<int:id>/', PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/like/', BlogLikeDislikeView.as_view(), name='post_likes'),
    path("posts/<int:blog_id>/comments/", CommentListCreateView.as_view(), name="comment_list_create"),
    path("posts/<int:post_id>/comments/<int:pk>/", CommentDetailView.as_view(), name="blog_detail"),
    # path('posts/<int:pk>/comments/create/', CommentCreate.as_view(), name='comment_create'),
    # path('posts/<int:pk>/comments/', CommentList.as_view(), name='comment_get'),
    # path('posts/<int:pk>/comment/<int:pk>/', CommentList.as_view(), name='comment_get'),

]
