from rest_framework import viewsets
from .models import User, FaceProfile
from .serializers import UserSerializer, FaceProfileSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class FaceProfileViewSet(viewsets.ModelViewSet):
    queryset = FaceProfile.objects.all()
    serializer_class = FaceProfileSerializer
