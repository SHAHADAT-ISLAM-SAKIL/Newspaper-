from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_ROLES = (
        ('subscriber', 'Subscriber'),
        ('editor', 'Editor'),
    )
    role = models.CharField(max_length=10, choices=USER_ROLES, default='subscriber')
    def __str__(self):
        return self.username

    def is_editor(self):
        return self.role == 'editor'

    def is_subscriber(self):
        return self.role == 'subscriber'
