from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'message', 'created']
    list_filter = ['created']
    search_fields = ['email', 'first_name', 'last_name']


admin.site.register(Contact, ContactAdmin)
