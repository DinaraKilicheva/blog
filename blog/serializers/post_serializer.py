from rest_framework import serializers

from blog.models import Post, LikeDislike
from blog.serializers.comment_serializer import CommentSerializer
from common.models import Category


#
# from blogs.models import Post, Comment, LikeDislike
#
#
# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ("id", "blog", "user", "body", 'parent')
#
#
# class CommentsDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ("id", "blog", "user", "body", 'parent')
#         read_only_fields = ("id",)
#
#
# class BlogLikeDislikeSerializer(serializers.Serializer):
#     type = serializers.ChoiceField(choices=LikeDislike.LikeType.choices)
#
#
# class PostSerializer(serializers.ModelSerializer):
#     comments = CommentSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Post
#         fields = ['title', 'body', 'author', 'category', 'comments', 'likes', 'dislikes']

class PostCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title")


class PostSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ["id", "title", "slug", "author", "category", "image", "views", "likes", "dislikes", "comments"]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["category"] = PostCategorySerializer(instance.category).data
        return data


class PostListSerializer(serializers.ModelSerializer):
    category = PostCategorySerializer()
    
    class Meta:
        model = Post
        fields = ["id", "title", "slug", "author", "category", "image", "views", "likes", "dislikes"]


class PostCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Post
        fields = ["id", "title", "author", "category"]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["category"] = PostCategorySerializer(instance.category).data
        return data


class BlogLikeDislikeSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=LikeDislike.LikeDislikeTypes.choices)
