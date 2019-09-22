from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Category, Tag, Comment, Photo


class InLinePhoto(admin.StackedInline):
    model = Photo
    extra = 1
    can_delete = True
    show_change_link = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    # Show image in the list of the posts
    def image_tag(self, obj):
        return format_html(f'<img src="{obj.featured_image.url}", width="120px", height="auto" />')

    image_tag.short_description = 'featured_image'

    # Fields Customisations
    fieldsets = (
        ('General', {
            'fields': (
                'author',
                'title',
                'slug',
                'description',
                'published',
                'featured'
            )
        }),
        ('Details', {
            'fields': (
                'content',
                'featured_image',
            )
        }),
        ('Filters', {
            'fields': (
                'categories',
                'tags',
            )
        }),
    )
    list_display = ['image_tag', 'title', 'author', 'featured', 'published', 'created']
    list_display_links = ['title', 'author']
    list_editable = ['published', 'featured']
    search_fields = ['title']
    list_filter = ['published', 'featured', 'created']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories', 'tags')

    # Inlines
    inlines = [InLinePhoto]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'post', 'content', 'reply_id', 'timestamp']
    list_filter = ['timestamp']
    search_fields = ['content']


admin.site.register(Category)
admin.site.register(Tag)

# Admin Site Custom Header
admin.site.site_header = 'Web Marketing Administration'
admin.site.site_title = 'Web Marketing Administration'
