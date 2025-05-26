from django.shortcuts import render, redirect
from django.contrib import messages
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import CustomTokenObtainPairSerializer
from .forms import UserRegistrationForm, LoginForm
from .permissions import IsAdmin, IsInstructor, IsStudent
from rest_framework_simplejwt.tokens import AccessToken, TokenError
from django.contrib.auth import get_user_model
import logging

# Set up logging
logger = logging.getLogger(__name__)

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
    # Check for valid token in cookie
    token = request.COOKIES.get('access_token')
    if token:
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # Extract user_id from token
            User = get_user_model()
            user = User.objects.get(id=user_id)  # Query user from database
            logger.info(f"User {user.username} accessed login with valid token")
            return render(request, 'home.html', {
                'username': user.username,
                'role': user.role
            })
        except (TokenError, User.DoesNotExist) as e:
            logger.warning(f"Invalid token or user not found: {e}")
            # Clear invalid token
            response = render(request, 'login.html', {'form': LoginForm()})
            response.delete_cookie('access_token')
            return response
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            logger.info(f"Login attempt for username: {form.cleaned_data['username']}")
            serializer = CustomTokenObtainPairSerializer(data={
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password']
            })
            try:
                serializer.is_valid(raise_exception=True)
                token_data = serializer.validated_data
                response = render(request, 'home.html', {
                    'username': token_data['username'],
                    'role': token_data['role']
                })
                response.set_cookie(
                    'access_token',
                    token_data['access'],
                    httponly=True,
                    secure=True,  # Use HTTPS in production
                    samesite='Strict'
                )
                logger.info(f"Successful login for {token_data['username']}")
                return response
            except Exception as e:
                logger.error(f"Login failed: {e}")
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})

# Logout View
def logout_view(request):
    token = request.COOKIES.get('access_token')
    if token:
        try:
            access_token = AccessToken(token)
            access_token.blacklist()
            logger.info(f"Token blacklisted for user {access_token['user_id']}")
        except TokenError as e:
            logger.warning(f"Invalid token on logout: {e}")
            messages.error(request, 'Invalid token')
        response = redirect('login_form')
        response.delete_cookie('access_token')
        messages.success(request, 'Logged out successfully')
        return response
    logger.info("Logout attempted with no token")
    return redirect('login_form')

# Homepage API View
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdmin | IsInstructor | IsStudent])
def home(request):
    return Response({
        'username': request.user.username,
        'role': request.user.role,
        'message': f"Welcome {request.user.username} ({request.user.role})"
    })