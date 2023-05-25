from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'title']


class CategoryDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['id', 'title']