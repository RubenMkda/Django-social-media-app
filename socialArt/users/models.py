from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30,unique=True, default='')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

class Posts(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(max_length=300)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    url_image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def num_likes(self):
        return self.like_set.count()
    
class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

class FriendshipRequest(models.Model):
    id = models.AutoField(primary_key=True)
    from_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friendship_requests_sent')
    to_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='friendship_requests_received')
    
class Friend(models.Model):
    to_user = models.ForeignKey(CustomUser, models.CASCADE, related_name='friends')
    from_user = models.ForeignKey(CustomUser, models.CASCADE, related_name='_unused_friend_relation')

    def save(self, *args, **kwargs):
        super (HistoryPost, self).save(*args, **kwargs)
        if timezone.now() > self.history.expires_at:
            self.delete()