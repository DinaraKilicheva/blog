from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from blog.models import Comment
from blog.serializers.comment_serializer import CommentsDetailSerializer, CommentSerializer


class CommentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.order_by("-id")
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return CommentsDetailSerializer
        return CommentSerializer
    
    def perform_create(self, serializer):
        blog_id = self.kwargs.get("blog_id")
        return serializer.save(user=self.request.user, blog_id=blog_id)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()
    
    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return CommentsDetailSerializer
        return CommentSerializer


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]
