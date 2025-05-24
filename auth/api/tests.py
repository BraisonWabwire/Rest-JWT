from rest_framework.test import APITestCase
from django.urls import reverse
from api.models import User  # Make sure this path is correct

class AuthTestCase(APITestCase):
    def setUp(self):
        self.student = User.objects.create_user(username='john', password='pass123', role='student')
    
    def test_token_authentication(self):
        url = reverse('token_obtain_pair')  # Ensure this name is correct in urls.py
        response = self.client.post(url, {'username': 'john', 'password': 'pass123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)
