from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
# from rest_framework.test import APIClient

from blog.models import Post
from common.models import Category
from users.models import User

client = Client()
csrf_client = Client(enforce_csrf_checks=True)


class TestPostListView(TestCase):
    def setUp(self) -> None:
        self.author = User.objects.create_user(
            username="example",
            first_name="Ben",
            email="user@example.com",
            password="2332"
        )
        self.client.login(user=self.author, password=2332)
        client.force_login(user=self.author)
        
        self.category = Category.objects.create(title="Technology")
        self.post = Post.objects.create(
            title="New post",
            slug="new-post",
            author=self.author,
            content="AI new technology",
            category=self.category,
        )
        
        self.new_post_data = {
            "title": "New1 post",
            "slug": "new-post",
            "author": self.author.id,
            "category": self.category.id,
            "views": 3
        }
    
    def test_post_list(self):
        print("sdf")
        url = reverse("post_list")
        response = client.get(url)
        
        self.assertEqual(response.status_code, 200)
        response = client.post(url, data=self.new_post_data)
    
    def test_post_create(self):
        url = reverse("post_create")
        response = client.post(url, self.new_post_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], self.new_post_data["title"])
    
    def test_post_detail(self):
        url = reverse("post_detail", kwargs={'id': self.post.pk})
        
        response = client.get(url)
        
        self.assertEqual(response.status_code, 200)
    
    def test_post_update(self):
        
        url = reverse("post_detail", kwargs={'id': self.post.pk})
        data = {
            "title": "update_post",
            "slug": "updated-post",
            "author": self.author.id,
            "category": self.category.id,
            "views": 4
        }
        response = client.put(url, data=data, content_type="application/json")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], data["title"])

    def test_post_delete(self):
        url = reverse("post_detail", kwargs={'id': self.post.pk})
    
        response = client.delete(url)
    
        self.assertEqual(response.status_code, 204)

# class BlogTest(TestCase):
#     def setUp(self) -> None:
#         # self.client = APIClient()
#         self.category = Category.objects.create(title='test_title')
#         self.user = User.objects.create_user(
#             email='tests@gmail.com',
#             username='tests',
#             password='123456'
#         )
#         self.client.login(user=self.user)
#         self.post = Post.objects.create(
#             title='test_title1',
#             body='body',
#             author=self.user,
#             category=self.category
#         )
#
#         self.comment = Comment.objects.create(blog=self.post, user=self.user)
#
#         self.post_data = {
#             "title": 'test_title1',
#             "body": 'body',
#             "author": self.user,
#             "category": self.category
#         }
#
#         self.comment_data = {
#             "post": self.post,
#             "content": "string"
#         }
#
#         self.like_dislike = LikeDislike.objects.create(blog=self.post, user=self.user, type='1')
#         self.like_dislike_data = {
#             "type": -1
#         }
#
#     def test_post_list(self):
#         url = reverse('post_list')
#         response = self.client.get(url)
#
#         self.assertEqual(response.status_code, 200)
#
#     def test_post_create(self):
#         url = reverse('post_create')
#         response = self.client.post(url, data=self.post_data)
#
#         self.assertEqual(response.status_code, 201)
#
#     def test_post_detail(self):
#         url = reverse('post_detail', kwargs={'slug': self.post.slug})
#         response = client.get(url)
#
#         self.assertEqual(response.status_code, 200)
#
#     def test_post_liked(self):
#         url = reverse('post_likes', kwargs={'slug': self.post.slug})
#         response = client.post(url, data=self.like_dislike_data)
#
#         self.assertEqual(response.status_code, 201)
#
#     def test_comment_get(self):
#         self.client.login(user=self.user)
#         url = reverse('comment_list_create', kwargs={'slug': self.post.slug})
#         response = client.get(url)
#         self.assertEqual(response.status_code, 200)
#
#     def test_comment_create(self):
#         url = reverse('comment_list_create', kwargs={'slug': self.post.slug})
#         response = self.client.post(url, data=self.comment_data)
#
#         self.assertEqual(response.status_code, 201)
