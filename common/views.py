from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework.permissions import IsAdminUser
from django.shortcuts import render, get_object_or_404
from rest_framework import status
# from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView, Response
from rest_framework.permissions import IsAuthenticated
from .models import Category
from common.serializers import CategorySerializer, CategoryDetailSerializer


# Create your views here.

# class CategoryListView(generics.ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#
#
# class CategoryCreateView(generics.CreateAPIView):
#     permission_classes = [IsAdminUser]
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
class CategoryListCreateView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CategoryDetailView(APIView):
#     def get_object(self, pk):
#         return get_object_or_404(Category, pk=pk)
#
#     def get(self, request, *args, **kwargs):
#         pk = kwargs.get("pk")
#         # category = get_object_or_404(Category, pk=pk)
#         # serializer = CategorySerializer(category)
#         serializer = CategorySerializer(self.get_object(pk))
#         return Response(serializer.data)
#
#     permission_classes = [IsAdminUser]
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk")
#         serializer = CategorySerializer(instance=self.get_object(pk), data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk")
#         category = self.get_object(pk)
#         category.delete()
#         return Response("Deleted.", status=status.HTTP_204_NO_CONTENT)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "pk"
    
    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return CategoryDetailSerializer
        return CategorySerializer
