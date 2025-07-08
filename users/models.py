from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    
    #Custom user model that extends the default Django user model.
    is_organizer = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)
    
    class Meta:
        permissions = (
            ("can_view_events", "Can view events"),
            ('can_register_himself', 'Can register himself'),
            ('can_unregister_himself', 'Can unregister himself'),
            ('can_view_own_registrations', 'Can view own registrations'),
            ("can_create_event", "Can create event"),
            ("can_edit_own_event", "Can edit own event"),
            ("can_delete_own_event", "Can delete own event"),
            ('can_view_own_event_registrations', 'Can view own event registrations')
        )

    def __str__(self):
        return self.username
