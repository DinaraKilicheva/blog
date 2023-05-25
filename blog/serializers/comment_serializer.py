from rest_framework import serializers

from blog.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("id", "blog", "user", "content", 'parent')


class CommentsDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    read_only_fields = ("id",)
    
    class Meta:
        model = Comment
        fields = ("id", "blog", "content")
        read_only_fields = ("blog",)
