from django.shortcuts import render
from utils.weather import weather
from utils.sales import item
from posts.models import Post
import os
from django.http import JsonResponse
# Create your views here.
def main(request):
    w_city = request.GET.get('w_city', 'Seoul')    
    city = request.GET.get('city', 'Seoul')    
    kakao_script_key = os.getenv('kakao_script_key')
    kakao_key = os.getenv('kakao_key')
    context = weather(w_city)
    posts = Post.objects.filter(city=city).values()
    if w_city:
        context['selected_city'] = w_city
    context['kakao_script_key'] = kakao_script_key
    context['kakao_key'] = kakao_key
    context['posts'] = posts
    context['m_selected_city'] = city
    return render(request, 'main.html', context)

def main(request):
    city = request.GET.get('city', 'Seoul')
    context = weather(city)
    if city:
        context['selected_city'] = city
    return render(request, 'main.html', context)

def sales(request):
    return render(request, 'sales.html', {'items':item()} )
  
def get_posts_by_sido(request):
    sido = request.GET.get('sido')
    posts = Post.objects.filter(city=sido).values()
    data = {'posts': list(posts)} 
    return JsonResponse(data)
