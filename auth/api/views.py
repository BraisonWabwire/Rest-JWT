from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer


from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import IsAdmin, IsInstructor, IsStudent


from django.shortcuts import render, redirect
from .forms import UserRegistrationForm

from .forms import LoginForm 

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
 
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_form')  # or wherever you want to redirect
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})



import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm

def login_form(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Prepare data to send to JWT token endpoint
            data = {
                'username': form.cleaned_data['username'],
                'password': form.cleaned_data['password']
            }
            # Call your JWT token obtain API endpoint (assuming it's on the same server)
            response = requests.post(request.build_absolute_uri('/api/token/'), data=data)

            if response.status_code == 200:
                token_data = response.json()
                # Save tokens in session (or wherever you want)
                request.session['access'] = token_data['access']

                # Here you need to decode JWT or call your backend to get user role,
                # But to keep it simple, let's decode the token (requires PyJWT)
                import jwt
                try:
                    decoded = jwt.decode(token_data['access'], options={"verify_signature": False})
                    role = decoded.get('role', 'user')
                except Exception:
                    role = 'user'

                # Save role in session
                request.session['role'] = role
                request.session['username'] = form.cleaned_data['username']

                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def home(request):
    username = request.session.get('username')
    role = request.session.get('role')
    if not username:
        return redirect('login_form')
    return render(request, 'home.html', {'username': username, 'role': role})
