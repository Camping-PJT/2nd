from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Message
from .forms import ReplyMessageForm
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.shortcuts import redirect


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['receiver', 'content']
    success_url = '/my_messages/sent/'

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'my_messages/message_list.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(receiver=self.request.user)

class SentMessagesView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'my_messages/sent_messages.html'
    context_object_name = 'messages'

    def get_queryset(self):
        return Message.objects.filter(sender=self.request.user)



class ReplyMessageView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = ReplyMessageForm
    success_url = reverse_lazy('my_messages:sent_messages')

    def get_initial(self):
        initial = super().get_initial()
        User = get_user_model()
        sender = get_object_or_404(User, id=self.kwargs['sender_id'])
        initial['receiver'] = sender.id
        return initial

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.receiver = get_object_or_404(get_user_model(), id=self.kwargs['sender_id'])
        return super().form_valid(form)
    
def delete(request, message_pk):
    message = Message.objects.get(pk=message_pk)
    message.delete()
    if message.receiver == request.user:
        return redirect('my_messages:inbox_messages')
    elif message.sender == request.user:
        return redirect ('my_messages:sent_messages')

