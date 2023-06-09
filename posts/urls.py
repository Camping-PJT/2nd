from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:category>', views.category, name='category'),
    path('city/', views.city, name='city'),
    path('theme/', views.theme, name='theme'),
    path('create/', views.create, name='create'),
    path('<int:post_pk>/', views.detail, name='detail'),
    path('<int:post_pk>/likes/', views.likes, name='likes'),
    path('<int:post_pk>/visits/', views.visits, name='visits'),
    path('<int:post_pk>/delete/', views.delete, name='delete'),
    path('<int:post_pk>/update/', views.update, name='update'),
    path('search/', views.search, name='search'),
    path('tags/<int:tag_pk>/', views.tagged_posts, name='tagged_posts'),
    path('update_priority_lists/', views.update_priority_lists, name='update_priority_lists'),
]


