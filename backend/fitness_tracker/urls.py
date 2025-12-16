from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Import the JWT views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Import for media serving (only needed in development)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Your activities API
    path('api/', include('activities.urls')),
    
    # JWT Token Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Root welcome message
    path('', lambda request: JsonResponse({"message": "Welcome to the Fitness Tracker API! Visit /api/activities/ to start."})),
]

# Serve media files during development (DEBUG = True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)