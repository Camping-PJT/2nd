from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Message
from .forms import ReplyMessageForm
from django.urls import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    fields = ['receiver', 'content']

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        message_pk = self.object.pk
        return reverse('my_messages:send_detail', kwargs={'message_pk': message_pk})


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'accounts/profile.html'
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
    
    def get_success_url(self):
        message_pk = self.object.pk
        return reverse('my_messages:send_detail', kwargs={'message_pk': message_pk})
    
    
def delete(request, message_pk):
    message = Message.objects.get(pk=message_pk)
    message.delete()
    return redirect('accounts:profile', request.user)


def send_detail(request, message_pk):
    message = Message.objects.get(pk=message_pk)
    context = {
        'message': message,
    }
    return render(request, 'my_messages/send_detail.html', context)


def receive_detail(request, message_pk):
    message = Message.objects.get(pk=message_pk)
    context = {
        'message': message,
    }
    return render(request, 'my_messages/receive_detail.html', context)
