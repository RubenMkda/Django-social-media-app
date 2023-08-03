from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.test import TestCase
from django.urls import reverse

from http import HTTPStatus

from .forms import CustomUserCreationForm
from .models import CustomUser
from .constants.constants_test import USERNAME, PASSWORD, EMAIL

class CustomUserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(email=EMAIL, username=USERNAME)

    def test_str_representation(self):
        user = CustomUser.objects.get(email=EMAIL)
        self.assertEqual(str(user), 'testuser')

    def test_get_full_name(self):
        user = CustomUser.objects.get(email=EMAIL)

        full_name = user.get_full_name()
        self.assertEqual(full_name, ' ')

    def test_get_short_name(self):
        user = CustomUser.objects.get(email=EMAIL)
        short_name = user.get_short_name()
        self.assertEqual(short_name, '')

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

class CustomUserRegisterTest(TestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.form_class = CustomUserCreationForm

    def test_register_success(self):
        sample_data ={
            "email":EMAIL,
            "username":USERNAME,
            "password1":PASSWORD,
            "password2":PASSWORD
        }

        form = self.form_class(sample_data)

        user = get_user_model()

        if form.is_valid():
            form.save()
        
        self.assertEqual(user.objects.count(), 1)
