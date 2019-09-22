from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile', default='profile/default.jpg')

    def __str__(self):
        return f'{self.user.first_name.capitalize()} {self.user.last_name.upper()}'
