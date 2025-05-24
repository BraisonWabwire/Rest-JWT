from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import IsAdmin, IsInstructor, IsStudent

@api_view(['GET'])
@permission_classes([IsAdmin])
def admin_dashboard(request):
    return Response({"message": "Welcome, admin!"})

@api_view(['GET'])
@permission_classes([IsInstructor])
def instructor_dashboard(request):
    return Response({"message": "Welcome, instructor!"})

@api_view(['GET'])
@permission_classes([IsStudent])
def student_dashboard(request):
    return Response({"message": "Welcome, student!"})
