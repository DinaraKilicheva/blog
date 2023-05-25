from django.test import TestCase
from django.test import TestCase
from django.urls import reverse

from users.models import User


# from rest_framework.test import APIClient

class CategoryTest(TestCase):
    def setUp(self) -> None:
        self.category = {
            'title': 'SomeCategory'
        }
        # self.client = APIClient()
    
    def test_category_list(self):
        url = reverse('category-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
    
    def test_category_detail(self):
        user = User.objects.create_superuser(
            email='dinara@gmail.com',
            password='2332'
        )
        
        self.client.force_authenticate(user=user)
        
        url = reverse('category-detail')
        response = self.client.post(url, data=self.category)
        self.assertEqual(response.status_code, 201)
    
    def test_category_put(self):
        user = User.objects.create_superuser(
            email='dinara@gmail.com',
            password='2332'
        )
        data = {"title": "changed"}
        
        self.client.force_authenticate(user=user)
        
        url = reverse('category-detail', kwargs={'id': self.category.pk})
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 201)
    
    def test_category_delete(self):
        user = User.objects.create_superuser(
            email='dinara@gmail.com',
            password='2332'
        )
        
        self.client.force_authenticate(user=user)
        
        url = reverse('category-detail', kwargs={'id': self.category.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 201)
