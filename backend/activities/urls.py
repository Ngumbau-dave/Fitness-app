from django.urls import path
from .views import (
    ActivityListCreateView,
    ActivityRetrieveUpdateDestroyView,
    StatsView,
    ProfileView  # ← Correct import
)

urlpatterns = [
    path('', ActivityListCreateView.as_view(), name='activity-list-create'),
    path('<int:pk>/', ActivityRetrieveUpdateDestroyView.as_view(), name='activity-detail'),
    path('stats/', StatsView.as_view(), name='stats'),
    path('profile/', ProfileView.as_view(), name='profile'),  # ← Route for profile
]