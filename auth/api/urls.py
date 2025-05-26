from django.urls import path
from api.views import register,login_form,home
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', register, name='register'),
    path('login/', login_form, name='login_form'),
    path('home/', home, name='home'),

]
