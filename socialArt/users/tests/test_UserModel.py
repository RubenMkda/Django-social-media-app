from django.test import TestCase

from users.models import CustomUser
from users.constants.constants_test import USERNAME, EMAIL

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