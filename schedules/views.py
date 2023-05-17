from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Schedule, Post
from django.urls import reverse
from utils.map import get_latlng_from_address
import os
from django.contrib import messages
from django.contrib.auth import get_user_model


@login_required
def calendar(request):
    posts = Post.objects.all()
    users = get_user_model().objects.exclude(id=request.user.id)
    posts = Post.objects.all()
    kakao_script_key = os.getenv('kakao_script_key')
    user_id = request.user.id
    schedules = Schedule.objects.filter(user_id=user_id)
    latitude_list = []
    longitude_list = []
    
    for schedule in schedules:
        address = schedule.post.address
        latitude, longitude = get_latlng_from_address(address)
        latitude_list.append(latitude)
        longitude_list.append(longitude)
    
    context = {
        'posts': posts,
        'schedules': schedules,
        'kakao_script_key': kakao_script_key,
        'latitude_list': latitude_list,
        'longitude_list': longitude_list,
        'users': users,
    }
    return render(request, 'schedules/calendar.html', context)


@login_required
def create_schedule(request):
    users = get_user_model().objects.exclude(id=request.user.id)
    posts = Post.objects.all()
    if request.method == 'POST':
        post_id = request.POST['post_id']
        start = request.POST['start']
        end = request.POST['end']
        description = request.POST['description']
        participants = request.POST.getlist('participants')
        
        post = get_object_or_404(Post, id=post_id)
        
        schedule = Schedule(
            post=post,
            user=request.user,
            title=post.title,
            start=start,
            end=end,
            description=description,
            address=post.address,
            extra_address=post.extra_address
        )
        schedule.save()

        schedule.participants.set(participants)
        
        return redirect(reverse('schedules:calendar'))

    context = {
        'posts': posts,
        'users': users,
    }
    return render(request, 'schedules/calendar.html', context)


@login_required
def get_schedule_data(request):
    schedules = Schedule.objects.filter(user=request.user)
    data = []
    for schedule in schedules:
        url = reverse('schedules:update', kwargs={'schedule_id': schedule.id}) 
        event_data = {
            'title': schedule.title,
            'start': schedule.start.isoformat(),
            'end': schedule.end.isoformat(),
            'url': url
        }
        data.append(event_data)
    return JsonResponse(data, safe=False)


def update_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    users = get_user_model().objects.exclude(id=request.user.id)
    participants = schedule.participants.all()
    if request.method == 'POST':
        schedule.post_id = request.POST['post_id']
        schedule.title = schedule.post.title
        schedule.start = request.POST['start']
        schedule.end = request.POST['end']
        schedule.description = request.POST['description']

        schedule.save()
        return redirect('schedules:calendar') 

    context = {
        'schedule': schedule,
        'schedule_id': schedule_id,
        'participants': participants,
        'users': users,
    }
    
    return render(request, 'schedules/update.html', context)


@login_required
def detail_schedule(request, schedule_id):
    kakao_script_key = os.getenv('kakao_script_key')
    schedule = get_object_or_404(Schedule, id=schedule_id)
    address = schedule.address
    latitude, longitude = get_latlng_from_address(address)
    participants = schedule.participants.all()
    
    context = {
        'schedule': schedule,
        'kakao_script_key': kakao_script_key,
        'latitude': latitude,
        'longitude': longitude,
        'participants': participants,
    }
    
    return render(request, 'schedules/detail.html', context)


@login_required
def delete_schedule(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    if request.user == schedule.user:
        schedule.delete()
        messages.success(request, '일정이 삭제되었습니다.')
    else:
        messages.error(request, '일정을 삭제할 권한이 없습니다.')
    return redirect('schedules:calendar')
