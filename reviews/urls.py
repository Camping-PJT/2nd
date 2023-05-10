from django.urls import path
from . import views

app_name = 'reviews'
urlpatterns = [
    path('<int:post_pk>/create/', views.create, name='create'),
    path('<int:review_pk>/update/', views.update, name='update'),
    path('<int:review_pk>/delete/', views.delete, name='delete'),
]
