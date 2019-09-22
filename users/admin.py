from django.contrib import admin
from django.utils.html import format_html

from users.models import Profile


class ProfileAdmin(admin.ModelAdmin):
    def image_tag(self, obj):
        return format_html('<img src="{}", width="60px", height="auto" />'.format(obj.image.url))

    image_tag.short_description = 'image'

    list_display = ['image_tag', 'user']


admin.site.register(Profile, ProfileAdmin)
