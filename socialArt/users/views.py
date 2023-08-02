from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomUserCreationForm, PotsForm
from .models import Posts, Like, CustomUser, FriendshipRequest, Friend

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'pages/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'pages/login.html', {'form': form})

@login_required
def home(request):
    if request.method == 'POST':
        form = PotsForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PotsForm()
    user = request.user
    friends = user.friends.all()
    friend_ids = [friend.from_user.id for friend in friends]
    posts = Posts.objects.filter(user__in=friend_ids).exclude(user=user)
    friend_requests = request.user.friendship_requests_received.all()
    context = {
        'form' : form,
        'posts': posts,
        'friend_request_received': friend_requests,
        'friends': friends
        }
    return render(request, 'pages/home.html', {'context': context})

@login_required
def searh_users(request):
    query = request.GET.get('q')

    if query:
        users = CustomUser.objects.filter(Q(username__icontains=query) | Q(email__icontains=query)).exclude(id=request.user.id)
    else:
        users = []

    if request.method == 'POST':
        friend_id = request.POST.get('friend_id')
        friend = CustomUser.objects.get(id=friend_id)
        FriendshipRequest.objects.create(from_user=request.user, to_user=friend)
        return redirect('search')

    return render(request, 'pages/search_users.html', {'users': users})

@login_required
def accept_friend_request(request, friend_request_id):
    friend_request = FriendshipRequest.objects.get(id=friend_request_id)

    Friend.objects.create(
        to_user=request.user,
        from_user=friend_request.from_user
    )

    Friend.objects.create(
        to_user=friend_request.from_user,
        from_user=request.user
    )

    friend_request.delete()

    return redirect('home')

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    user = request.user

    if len(Like.objects.filter(user=user, post=post)) == 1:
        return redirect(request.META.get('HTTP_REFERER'))
    
    like = Like(user=user, post=post)
    like.save()

    return redirect(request.META.get('HTTP_REFERER'))

def index(request):
    return render(request, 'pages/index.html')