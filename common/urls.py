from django.urls import path

from common.views import CategoryListCreateView, CategoryDetailView

urlpatterns = [
    path("", CategoryListCreateView.as_view(), name='category-list'),
    path("detail/<int:pk>/", CategoryDetailView.as_view(), name='category-detail'),
]