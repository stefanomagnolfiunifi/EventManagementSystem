from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home') # Redirect to the home page after login
        else:
            return render(request, 'users/login.html', {'error': 'Credenziali errate'})
    return render(request, 'users/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user.is_organizer:
                group = Group.objects.get(name='Organizers')
            else:
                group = Group.objects.get(name='Attendees')
            group.user_set.add(user)
            print("User registered successfully")
            return redirect('login')
        else:
            print("Form is not valid")
            print(form.errors)
            return render(request, 'users/signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'users/signup.html', {'form': form})


@login_required
def profile_view(request):
    user = request.user
    user_fields = {
        'Username': user.username,
        'Email': user.email if user.email else 'N/A',
        'Date of Birth': user.date_of_birth if user.date_of_birth else 'N/A',
        'Role': 'Organizer' if user.is_organizer else 'Attendee'
    }
    return render(request, 'users/profile.html', {'user_fields': user_fields})    

@login_required
def custom_logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')