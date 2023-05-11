from django.urls import path
from . import views

app_name = 'schedules'
urlpatterns = [
    path('calendar/', views.calendar, name='calendar'),
]
