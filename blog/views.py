from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import modelformset_factory, inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .forms import PostForm, CommentForm
from .filters import PostFilter
from .models import Post, Comment, Photo


class PostListView(ListView):
    queryset = Post.objects.filter(published=True)
    template_name = 'search/post-list.html'
    title = 'All Articles'
    extra_context = {
        'title': title,
        'posts': queryset
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context


class UserPostView(LoginRequiredMixin, ListView):
    login_url = 'sign_in'
    redirect_field_name = 'redirect_to'
    template_name = 'user-posts.html'
    context_object_name = 'user_posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostFeaturedView(ListView):
    title = 'Featured Articles'
    queryset = Post.objects.filter(featured=True, published=True).order_by('-created')[:4]
    template_name = 'featured-posts.html'
    context_object_name = 'featured_posts'

    extra_context = {
        'title': title
    }


def post_detail_view(request, slug):
    template_name = 'post-detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = Comment.objects.filter(post=post, reply=None).order_by('-timestamp')
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(post=post, user=request.user, content=content, reply=comment_qs)
            comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, template_name, context)


class CreatePostView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'sign_in'
    redirect_field_name = 'redirect_to'
    template_name = 'post-create.html'
    form_class = PostForm
    model = Post
    slug_field = 'slug'
    success_message = 'Article successfully Created'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreatePostView, self).form_valid(form)


class UpdatePostView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = 'sign_in'
    redirect_field_name = 'redirect_to'
    template_name = 'post-update.html'
    form_class = PostForm
    model = Post
    slug_field = 'slug'
    success_message = 'Article successfully updated'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(UpdatePostView, self).form_valid(form)


class DeletePostView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = 'sign_in'
    redirect_field_name = 'redirect_to'
    template_name = 'post_confirm_delete.html'
    model = Post
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = '/blog/articles/'
    success_message = 'Article successfully deleted'
