from django.db import models
from django.conf import settings

#Model representing an event
class Event(models.Model):

    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=100)
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='organized_events'
    )
    registrations = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='attending_events', 
        blank=True
    )

    def __str__(self):
        return self.title