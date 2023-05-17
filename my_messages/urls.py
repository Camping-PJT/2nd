from django.urls import path
from .views import MessageCreateView, MessageListView, SentMessagesView, ReplyMessageView
from . import views

app_name = 'my_messages'
urlpatterns = [
    path('send/', MessageCreateView.as_view(), name='send_message'),
    path('inbox/', MessageListView.as_view(), name='inbox_messages'),
    path('sent/', SentMessagesView.as_view(), name='sent_messages'),
    path('reply/<int:sender_id>/', ReplyMessageView.as_view(), name='reply'),
    path('<int:message_pk>/delete/', views.delete, name='delete'),
]


