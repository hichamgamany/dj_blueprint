from .models import Post, Category, Tag
from django import forms
import django_filters


class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(label='Search by title',
                                      lookup_expr='icontains',
                                      widget=forms.TextInput(attrs={'placeholder': 'Search by Title'}))

    categories = django_filters.ModelMultipleChoiceFilter(queryset=Category.objects.all(),
                                                          widget=forms.CheckboxSelectMultiple(attrs={'class': 'uk-checkbox'}))

    tags = django_filters.ModelMultipleChoiceFilter(queryset=Tag.objects.all(),
                                                    widget=forms.CheckboxSelectMultiple(attrs={'class': 'uk-checkbox'}))

    class Meta:
        model = Post
        fields = ['title', 'categories', 'tags']
