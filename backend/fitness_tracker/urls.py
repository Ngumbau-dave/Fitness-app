from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Import JWT views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Import your new views
from activities.views import (
    ActivityListCreateView,
    ActivityRetrieveUpdateDestroyView,
    StatsView,
    ProfileView,
    RegisterView,
)

# Import for media (avatars)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Activities endpoints (direct, no separate activities.urls needed)
    path('api/activities/', ActivityListCreateView.as_view(), name='activity_list_create'),
    path('api/activities/<int:pk>/', ActivityRetrieveUpdateDestroyView.as_view(), name='activity_detail'),
    
    # New endpoints
    path('api/stats/', StatsView.as_view(), name='stats'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
    path('api/register/', RegisterView.as_view(), name='register'),
    
    # JWT Token Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Root welcome message
    path('', lambda request: JsonResponse({"message": "Welcome to the Fitness Tracker API! Visit /api/activities/ to start."})),
]

# Serve media files (avatars) in development and production on Render
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)