from django.shortcuts import render,redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .models import Schedule

# Create your views here.


def calendar(request):
    return render(request, 'schedules/calendar.html')