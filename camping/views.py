from django.shortcuts import render
from utils.weather import weather


# Create your views here.

def main(request):
    city = request.GET.get('city', 'Seoul')
    context = weather(city)
    if city:
        context['selected_city'] = city
    return render(request, 'main.html', context)