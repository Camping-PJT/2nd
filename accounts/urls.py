from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('update/', views.update, name='update'),
    path('delete/', views.delete, name='delete'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('password/', views.change_password, name='change_password'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('<int:user_pk>/follow/', views.follow, name='follow'),
    path('profile/<str:username>/following-list/', views.following_list, name='following_list'),
    path('profile/<str:username>/followers-list/', views.followers_list, name='followers_list'),
    path('priority_list/<str:username>/', views.priority_list, name='priority_list'),
]
