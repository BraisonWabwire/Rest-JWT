from django.urls import path
from .views import register, login_form, home, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/home/', home, name='home'),
    path('', register, name='register'),
    path('login/', login_form, name='login_form'),
]