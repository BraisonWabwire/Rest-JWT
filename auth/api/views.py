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
from rest_framework_simplejwt.tokens import AccessToken, TokenError

def login_form(request):
    # Check for valid token in cookie
    token = request.COOKIES.get('access_token')
    if token:
        try:
            access_token = AccessToken(token)
            user = access_token.user
            return render(request, 'home.html', {
                'username': user.username,
                'role': user.role
            })
        except TokenError:
            pass  # Invalid token, proceed to login
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = {
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password']
            }
            try:
                response = requests.post(request.build_absolute_uri('/api/token/'), data=data)
                response.raise_for_status()
                token_data = response.json()
                response = render(request, 'home.html', {
                    'username': token_data['username'],
                    'role': token_data['role']
                })
                response.set_cookie(
                    'access_token',
                    token_data['access'],
                    httponly=True,
                    secure=True,
                    samesite='Strict'
                )
                return response
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