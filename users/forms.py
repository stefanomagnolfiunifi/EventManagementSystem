from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser 


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email','is_organizer')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_organizer = self.cleaned_data.get('is_organizer', False)
        
        if commit:
            user.save()
        return user