from django import forms
from django.contrib.auth import get_user_model
from .models import Event

User = get_user_model()

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter event title',
                'maxlength': '100'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Describe your event...',
                'rows': 4
            }),
            'date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Event location',
                'maxlength': '100'
            })
        }
        labels = {
            'title': 'Event Title',
            'description': 'Event Description',
            'date': 'Date & Time',
            'location': 'Location'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set help texts for fields
        self.fields['title'].help_text = 'Maximum 100 characters'
        self.fields['date'].help_text = 'Select date and time for the event'
        
        # Make all fields required
        for field in self.fields.values():
            field.required = True

    def clean_date(self):
        # Date field vaidation
        from django.utils import timezone
        date = self.cleaned_data.get('date')
        
        if date and date < timezone.now():
            raise forms.ValidationError("Event date cannot be in the past.")
        
        return date

    def clean_title(self):
        # Title field validation
        title = self.cleaned_data.get('title')
        
        if title and len(title.strip()) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        
        return title.strip() if title else title

    def save(self, organizer):
        
        event = super().save(commit=False)
        
        if organizer:
            event.organizer = organizer
        
        
        event.save()
            
        return event

   