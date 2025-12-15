from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Import the JWT views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Your existing activities API
    path('api/', include('activities.urls')),  # Note: I changed 'api' to 'api/' – this is better practice and might fix your /api/activities/ 404 if it was a trailing slash issue
    
    # JWT Token Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # POST here for login (username/password → access + refresh tokens)
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Optional: POST refresh token to get new access token
    
    # Root welcome message
    path('', lambda request: JsonResponse({"message": "Welcome to the Fitness Tracker API! Visit /api/activities/ to start."})),
]