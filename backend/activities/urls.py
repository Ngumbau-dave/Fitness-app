from django.urls import path
from .views import (
    ActivityListCreateView,
    ActivityRetrieveUpdateDestroyView,
    RegisterView,
    StatsView,
    ProfileView
)

urlpatterns = [
    path('', ActivityListCreateView.as_view(), name='activity-list-create'),
    path('<int:pk>/', ActivityRetrieveUpdateDestroyView.as_view(), name='activity-detail'),
    path('register/', RegisterView.as_view(), name='register'),  # ← Registration endpoint
    path('stats/', StatsView.as_view(), name='stats'),
    path('profile/', ProfileView.as_view(), name='profile'),
]