from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser 
from dateutil.relativedelta import relativedelta


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email','is_organizer', 'date_of_birth')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter username',
                'maxlength': '100'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }
        labels = {
            'is_organizer': 'I am an Organizer',
            'date_of_birth': 'Date of Birth',
        }


    def clean_date_of_birth(self):
        # Date field vaidation
        date = self.cleaned_data.get('date_of_birth')
        
        today = date.today()
        max_allowed_date = today - relativedelta(years=14)
        if date > max_allowed_date:
            raise forms.ValidationError("You need to be at least 14 years old.")
        
        return date

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_organizer = self.cleaned_data.get('is_organizer', False)
        user.date_of_birth = self.cleaned_data.get('date_of_birth', False)
        
        if commit:
            user.save()
        return user