from django.urls import path
from api import views
from .views import CustomTokenObtainPairView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('admin/dashboard/', views.admin_dashboard),
    path('instructor/dashboard/', views.instructor_dashboard),
    path('student/dashboard/', views.student_dashboard),
]
