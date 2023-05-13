from django.urls import path
from . import views

app_name = 'schedules'
urlpatterns = [
    path('calendar/', views.calendar, name='calendar'),
    path('create/', views.create_schedule, name='create'),
    path('update/<int:schedule_id>/', views.update_schedule, name='update'),
    path('delete/<int:schedule_id>/', views.delete_schedule, name='delete'),
    path('get_schedule_data/', views.get_schedule_data, name='get_schedule_data'),
]