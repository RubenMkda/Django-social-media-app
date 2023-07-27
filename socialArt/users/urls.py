from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('loguot', auth_views.LogoutView.as_view(next_page='login'), name='logout' ),
    path('home/', views.home, name='home'),
]