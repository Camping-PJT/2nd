from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash, authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm, CustomAuthenticationForm
from posts.models import Post
from django.http import JsonResponse
from schedules.models import Schedule
import os
from django.urls import reverse_lazy
from posts.models import Priority
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.utils import timezone
from django.core import serializers
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from my_messages.models import Message


# Create your views here.

def signup(request):
    if request.user.is_authenticated:
        return redirect('posts:index')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.address = request.POST.get('address')
            user.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/signup.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            prev_url = request.session.get('prev_url')
            if prev_url:          
                del request.session['prev_url']
                return redirect(prev_url)
            return redirect('main')
        return redirect('accounts:login')
    else:
        form = CustomAuthenticationForm()
        request.session['prev_url'] = request.META.get('HTTP_REFERER')
    context = {
        'form': form,
    }
    return render(request, 'accounts/login.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return redirect('main')
    

@login_required
def delete(request):
    request.user.delete()
    return redirect('main')


@login_required
def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.address = request.POST.get('address')
            user.save()
            return redirect('accounts:profile', request.user.username)
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/update.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('main')
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {
        'form': form,
    }
    return render(request, 'accounts/change_password.html', context)

    
@login_required
def profile(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    user_id = request.user.id
    like_post = person.like_posts.all()
    liked_posts = like_post.exclude(priority__user=request.user)
    # priority_range = range(1, 11)
    # priority_range2 = range(6, 11)
    priorities = Priority.objects.filter(user=request.user).order_by('priority')
    schedules = Schedule.objects.filter(user_id=user_id, start__gte=timezone.now()).order_by('start__date', 'end__date')
    messages = Message.objects.filter(receiver=request.user)
    sentmessages = Message.objects.filter(sender=request.user)

    context = {
        'person': person,
        'followings': person.followings.all(),
        'followers': person.followers.all(),
        'priorities': priorities,
        'schedules': schedules,
        'liked_posts': liked_posts,
        # 'priority_range': priority_range,
        # 'priority_range2': priority_range2,
        'messages': messages,
        'sentmessages': sentmessages,
    }

    return render(request, 'accounts/profile.html', context)



@login_required
def follow(request, user_pk):
    User = get_user_model()
    person = User.objects.get(pk=user_pk)

    if person != request.user:
        if request.user in person.followers.all():
            person.followers.remove(request.user)
            is_followed = False
        else:
            person.followers.add(request.user)
            is_followed = True
        context = {
            'is_followed': is_followed,
            'followings_count': person.followings.count(),
            'followers_count': person.followers.count(),
        }
        return JsonResponse(context)
    return redirect('accounts:profile', person.username)


@login_required
def following_list(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    followings = person.followings.all()
    context = {
        'followings': followings,
        }
    return render(request, 'accounts/following_list.html', context)


@login_required
def followers_list(request, username):
    User = get_user_model()
    person = User.objects.get(username=username)
    followers = person.followers.all()
    context = {
        'followers': followers,
        }
    return render(request, 'accounts/followers_list.html', context)

def priority_list(request, username):
    user_id = request.user.id
    User = get_user_model()
    person = User.objects.get(username=username)
    priorities = Priority.objects.filter(user=person).order_by('priority')
    data = []
    for priority in priorities:
        post_data = serializers.serialize('python', [priority.post])[0]
        post = post_data['fields']
        post['pk'] = post_data['pk']
        data.append({'post': post})
    return JsonResponse(data, safe=False)

