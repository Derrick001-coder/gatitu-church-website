from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomUserLoginForm, ProfileUpdateForm, AvatarUploadForm
def custom_login(request):
    if request.method == 'POST':
        form = CustomUserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Authenticate user
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                return redirect('home')
            else:
                # Add error message for invalid credentials
                messages.error(request, 'Invalid email or password. Please try again.')
        else:
            # Form validation errors (like empty fields)
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

def custom_logout(request):
    auth_logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # SIMPLE FIX: Redirect to login page instead of auto-login
            messages.success(request, f'Account created successfully! Welcome to PCEA Gatitu Church, {user.get_full_name()}! Please login with your credentials.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST' and 'avatar' in request.FILES:
        # Handle avatar upload separately
        form = AvatarUploadForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile photo updated successfully!')
            return redirect('profile')
    return render(request, 'users/profile.html')

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'users/update_profile.html', {'form': form})