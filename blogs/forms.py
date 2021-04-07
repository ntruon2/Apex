from django.conf import settings
from django import forms

from .models import Blog

MAX_BLOG_LENGTH = settings.MAX_BLOG_LENGTH

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > MAX_BLOG_LENGTH:
            raise forms.ValidationError("This blog is too long")
        return content
