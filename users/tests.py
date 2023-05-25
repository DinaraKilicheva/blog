from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIClient

from users.models import User

client = Client()


class UserRegistrationTest(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="example",
            first_name="Ben",
            email="user@example.com",
            is_admin=True,
            is_staff=True,
        )
    
    def test_user_register(self):
        new_user_data = {
            "email": "rest@example.com",
            "first_name":"dinara",
            "username": 'Ben',
            "password1": '2332',
            "password2": '2332',
        }
        
        url = reverse('register')
        response = client.post(url, data=new_user_data)
        self.assertEqual(response.status_code, 201)
    
    def test_user_login(self):
        # user = User.objects.create_user(
        #     email='rest@example.com',
        #     username='Ben',
        #     password='2332'
        # )
        
        data = {
            "email": "rest@example.com",
            "password": "2332"
        }
        url = reverse('token_obtain_pair')
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, 201)
    
    def test_user_profil(self):
        self.client = APIClient()
        # user = User.objects.create_user(
        #     email='rest@example.com',
        #     username='userjon',
        #     password='2332'
        # )
        
        url = reverse('profile', kwargs={'id': self.user.pk})
        
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
