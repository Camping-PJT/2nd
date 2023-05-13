from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Schedule, Post
from django.urls import reverse


# Create your views here.


def calendar(request):
    posts = Post.objects.all()  
    user_id = request.user.id
    schedules = Schedule.objects.filter(user_id=user_id)
    context = {
        'posts': posts,  
        'schedules': schedules
    }
    return render(request, 'schedules/calendar.html', context)


def create_schedule(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        start = request.POST['start']
        end = request.POST['end']
        description = request.POST['description']
        
        post = get_object_or_404(Post, id=post_id)
        schedule = Schedule(post=post, user=request.user, title=post.title, start=start, end=end, description=description)
        schedule.save()
        
        return redirect(reverse('schedules:calendar'))
    
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    return render(request, 'schedules/create.html', context)


def get_schedule_data(request):
    schedules = Schedule.objects.filter(user=request.user)  # 현재 사용자가 작성한 스케줄만 필터링
    data = [
        {
            'title': schedule.title,
            'start': schedule.start.isoformat(),
            'end': schedule.end.isoformat()
        }
        for schedule in schedules
    ]
    return JsonResponse(data, safe=False)


def update_schedule(request, schedule_id):
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    if request.method == 'POST':
        schedule.post_id = request.POST['post_id']
        schedule.start = request.POST['start']
        schedule.end = request.POST['end']
        schedule.description = request.POST['description']
        schedule.save()
        return redirect('schedules:calendar')
    context = {
        'schedule': schedule
    }
    return render(request, 'schedules/update.html', context)


def delete_schedule(request, schedule_id):
    schedule = Schedule.objects.get(id=schedule_id)
    if request.user == schedule.user:
        schedule.delete()
    return redirect('schedules:calendar')