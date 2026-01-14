from rest_framework import generics, permissions
from .serializers import UserRegistrationSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    # Allow anyone to hit this endpoint to sign up
    permission_classes = [permissions.AllowAny]