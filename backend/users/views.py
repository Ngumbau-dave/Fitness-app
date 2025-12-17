from .serializers import UserSerializer  # Add this import in views.py
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    # ... rest unchanged