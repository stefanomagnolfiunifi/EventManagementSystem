from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    
    #Custom user model that extends the default Django user model.
    is_organizer = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
