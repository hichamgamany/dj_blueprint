from django.urls import path
from .views import home_view, contact_view, contact_email_received

urlpatterns = [
    path('', home_view, name='home_view'),
    path('contact/', contact_view, name='contact_view'),
    path('contact_email_received/', contact_email_received, name='contact_email_received'),
]
