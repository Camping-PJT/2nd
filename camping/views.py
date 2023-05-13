from django.shortcuts import render
from utils.weather import weather
from utils.sales import item


# Create your views here.

def main(request):
    city = request.GET.get('city', 'Seoul')
    context = weather(city)
    if city:
        context['selected_city'] = city
    return render(request, 'main.html', context)

def sales(request):
    return render(request, 'sales.html', {'items':item()} )