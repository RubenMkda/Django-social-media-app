from django.test import TestCase

from users.constants.constants_test import USERNAME
from users.models import CustomUser, Posts, Like

class PostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = CustomUser.objects.create(username=USERNAME)
        cls.user2 = CustomUser.objects.create(username='pepito')
        cls.post = Posts.objects.create(content='Test Content', user=cls.user)

    def test_num_likes(self):
        post = Posts.objects.get(id=self.post.id)
        user = self.user

        Like(user=user, post=post)

        self.assertIsNot(post.num_likes(), 1)