from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CustomTokenObtainPairSerializer
from .forms import UserRegistrationForm, LoginForm
from .permissions import IsAdmin, IsInstructor, IsStudent
import requests

# Custom Token View
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Registration View
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login_form')
        else:
            messages.error(request, 'Registration failed. Please check the form.')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# Login View
def login_form(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = {
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password']
            }
            try:
                # Call the JWT token endpoint
                response = requests.post(request.build_absolute_uri('/api/token/'), data=data)
                response.raise_for_status()
                token_data = response.json()
                
                # Pass the access token and role to the template via a redirect
                return render(request, 'home.html', {
                    'access_token': token_data['access'],
                    'username': token_data['username'],
                    'role': token_data['role']
                })
            except requests.RequestException:
                messages.error(request, 'Error connecting to authentication server')
            except Exception:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

# Homepage API View (protected by JWT and role)
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin | IsInstructor | IsStudent])
def home(request):
    return Response({
        'username': request.user.username,
        'role': request.user.role,
        'message': f"Welcome {request.user.username} ({request.user.role})"
    })