from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from users.forms import CustomUserCreationForm
from users.constants.constants_test import USERNAME, PASSWORD, EMAIL

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