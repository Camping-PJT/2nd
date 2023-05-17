from django import forms
from .models import Message
from django.contrib.auth import get_user_model

class MessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(queryset=get_user_model().objects.all(), empty_label=None)

    class Meta:
        model = Message
        fields = ['receiver', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }


class ReplyMessageForm(forms.ModelForm):
    receiver = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.Select(attrs={'readonly': True})
    )
    class Meta:
        model = Message
        fields = ['receiver', 'content']
