from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('loguot', auth_views.LogoutView.as_view(next_page='login'), name='logout' ),
    path('home/', views.home, name='home'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('accept_friend/<int:friend_request_id>/', views.accept_friend_request, name='accept_friend'),
    path('search/', views.searh_users, name='search')
]