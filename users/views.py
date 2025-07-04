from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('events:event_list')
        else:
            return render(request, 'users/login.html', {'error': 'Credenziali errate'})
    return render(request, 'users/login.html')

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("User registered successfully")
            return redirect('login')
        else:
            print("Form is not valid")
            print(form.errors)
            return render(request, 'users/signup.html', {'form': form})
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'users/signup.html', {'form': form})

def custom_logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('login')