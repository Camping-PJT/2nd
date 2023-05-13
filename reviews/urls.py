from django.urls import path
from . import views

app_name = 'reviews'
urlpatterns = [
    path('<int:post_pk>/create/', views.create, name='create'),
    path('<int:review_pk>/update/', views.update, name='update'),
    path('<int:review_pk>/', views.detail, name='detail'),
    path('<int:review_pk>/delete/', views.delete, name='delete'),
    # path('<int:review_pk>/emotes/<int:emotion>/', views.emotes, name='emotes'),
    path('<int:review_pk>/likes/', views.review_likes, name='review_likes'),
    path('<int:review_pk>/dislikes/', views.review_dislikes, name='review_dislikes'),
]
