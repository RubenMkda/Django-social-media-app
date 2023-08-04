from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from users.constants.constants_test import USERNAME, EMAIL, PASSWORD

class CustomUserLoginTest(TestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.user = get_user_model().objects.create(
            email=EMAIL,
            username=USERNAME,
            password=PASSWORD
            )
    
    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': EMAIL,
            'password': PASSWORD
        })

        self.assertEqual(response.status_code, 200)

    def test_login_failure(self):
        response = self.client.post(self.login_url, {
            'username': 'incorret',
            'password': 'wrongpassword'
        })

        self.assertTemplateUsed(response, 'pages/login.html')