from django.shortcuts import render
from utils.weather import weather
from utils.sales import item
from posts.models import Post, Facility
import os
from django.http import JsonResponse
# Create your views here.
def main(request):
    allpost = Post.objects.all()
    w_city = request.GET.get('w_city', 'Seoul')    
    city = request.GET.get('city', 'Seoul')    
    kakao_script_key = os.getenv('kakao_script_key')
    kakao_key = os.getenv('kakao_key')
    context = weather(w_city)
    posts = Post.objects.filter(city=city).values()
    choices = Facility.FACILITY_CHOICES
    facilities = [ choice[1] for choice in choices]
    if w_city:
        context['selected_city'] = w_city
    context['kakao_script_key'] = kakao_script_key
    context['kakao_key'] = kakao_key
    context['posts'] = posts
    context['m_selected_city'] = city
    context['allpost'] = allpost
    context['facilities'] = facilities

    outdoor_posts = Post.objects.filter(category='오지, 노지').count()
    paycamp_posts = Post.objects.filter(category='유료').count()
    caravan_posts = Post.objects.filter(category='글램핑, 카라반').count()
    total_posts = outdoor_posts + paycamp_posts + caravan_posts

    if total_posts == 0:
        caravan_percentage=paycamp_percentage=outdoor_percentage = 100
    else:
        outdoor_percentage = (outdoor_posts / total_posts) * 100
        paycamp_percentage = (paycamp_posts / total_posts) * 100
        caravan_percentage = (caravan_posts / total_posts) * 100

    context['outdoor_percentage'] = outdoor_percentage
    context['paycamp_percentage'] = paycamp_percentage
    context['caravan_percentage'] = caravan_percentage

    return render(request, 'main.html', context)

def sales(request):
    return render(request, 'sales.html', {'items':item()} )
  
def get_posts_by_sido(request):
    sido = request.GET.get('sido')
    posts = Post.objects.filter(city=sido).values()
    data = {'posts': list(posts)} 
    return JsonResponse(data)
