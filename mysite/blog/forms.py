from django.forms import ModelForm
from .models import Post, Message
from django import forms


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['author', 'likes']

    def __init__(self, *args, **kwargs) -> None:
        super(PostForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs['placeholder'] = 'e.g. Python Tutorial For Beginners'
        self.fields['description'].widget.attrs['placeholder'] = 'Enter your description'
        self.fields['topic'].widget.attrs['placeholder'] = 'Enter or select a topic'


class ReplyForm(ModelForm):
    class Meta:
        model = Message
        fields = ['body']
