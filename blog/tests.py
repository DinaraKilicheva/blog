from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
# from rest_framework.test import APIClient

from blog.models import Post, LikeDislike, Comment
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
            password="2332",
            is_admin=True,
            is_staff=True,
        )
        
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
        self.like_dislike = LikeDislike.objects.create(post=self.post, user=self.author, type='1')
        
        self.like_dislike_data = {
            "type": -1
        }
        
        # self.comment = Comment.objects.create(
        #     user=self.author.id,
        #     content="wqw",
        #     post=self.post.id
        # )
        
    
    def test_post_list(self):
        print("sdf")
        url = reverse("post_list")
        response = client.get(url)
        
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, data=self.new_post_data)
    
    def test_post_create(self):
        url = reverse("post_create")
        response = self.client.post(url, self.new_post_data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["title"], self.new_post_data["title"])
    
    def test_post_detail(self):
        url = reverse("post_detail", kwargs={'id': self.post.pk})
        
        response = self.client.get(url)
        
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
        response = self.client.put(url, data=data, content_type="application/json")
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], data["title"])
    
    def test_post_delete(self):
        self.client.login(email=self.author.email, password="2332")
        url = reverse("post_detail", kwargs={'id': self.post.pk})
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, 204)
    
    def test_post_like(self):
        url = reverse('post_likes', kwargs={'id': self.post.pk})
        response = self.client.post(url, data=self.like_dislike_data)
        self.assertEqual(response.status_code, 201)
    
    # def test_comment_get(self):
    #     self.client.login(user=self.author)
    #     url = reverse('comment_list_create', kwargs={'blog_id': self.post.id})
    #     response = client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #
    # def test_comment_post(self):
    #     comment_data = {
    #         "some text"
    #     }
    #     url = reverse('comment_detail', kwargs={'blog_id': self.post.id, "id": self.comment.id})
    #     response = self.client.post(url, comment_data)
    #     self.assertEqual(response.status_code, 201)
