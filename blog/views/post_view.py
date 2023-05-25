from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.serializers.post_serializer import BlogLikeDislikeSerializer
from paginations import CustomPageNumberPagination
from blog.models import Post, LikeDislike
from blog.serializers.post_serializer import PostSerializer, PostListSerializer, PostCreateSerializer


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.order_by("-id")
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ("category", "author", "likes")
    ordering_fields = ("id", "title")
    search_fields = ("title", 'category__title')
    pagination_class = CustomPageNumberPagination
    
    serializer_class = PostListSerializer
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return PostCreateSerializer
        return PostListSerializer


class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer


class PostRetrieveView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class PostUpdateView(generics.UpdateAPIView):
    queryset = Post
    serializer_class = PostCreateSerializer
    lookup_field = "id"


class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    lookup_field = "id"


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    lookup_field = "id"
    
    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return PostCreateSerializer
        return PostListSerializer


class BlogLikeDislikeView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(request_body=BlogLikeDislikeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = BlogLikeDislikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        type_ = serializer.validated_data.get("type")
        type_detail = ''
        if type_ == '1':
            type_detail = 'liked'
        if type_ == '-1':
            type_detail = 'unliked'
        user = request.user
        blog = Post.objects.filter(slug=self.kwargs.get("slug")).first()
        if not blog:
            raise Http404
        like_dislike_blog = LikeDislike.objects.filter(blog=blog, user=user).first()
        if like_dislike_blog and like_dislike_blog.type == type_:
            like_dislike_blog.delete()
        else:
            LikeDislike.objects.update_or_create(blog=blog, user=user, defaults={"type": type_})
        data = {"type": type_, "detail": type_detail}
        return Response(data)
