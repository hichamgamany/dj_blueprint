from django import forms

from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            'title',
            'description',
            'content',
            'featured_image',
            'categories',
            'tags',
        )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {
            'content'
        }
