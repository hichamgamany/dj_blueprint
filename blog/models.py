from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=40, null=False, blank=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=40, null=False, blank=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=100, null=False, blank=False)
    slug = models.CharField(max_length=100, unique=True)
    featured_image = models.ImageField(upload_to='blog/featured_images', default='default.jpg')
    description = models.CharField(max_length=191, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    published = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_photo')
    photo = models.ImageField(upload_to='blog/%s' % post, default='default.jpg')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.post}"


def slug_generator(sender, instance, *args, **kwargs):
    slug = slugify(instance.title)
    # exists = Post.objects.filter(slug=slug).exists()
    # if exists:
    #     slug = "%s-%s" % (slug, instance.id)
    instance.slug = slug


pre_save.connect(slug_generator, sender=Post)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reply = models.ForeignKey('self', null=True, related_name='replies', on_delete=models.SET_NULL)
    content = models.CharField(max_length=250)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"post: {self.post}, comment: {self.content}"
