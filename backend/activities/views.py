from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated  # Only need AllowAny for testing
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from .models import Activity
from .serializers import ActivitySerializer

class ActivityListCreateView(generics.ListCreateAPIView):
    queryset = Activity.objects.all().order_by('-date')  # Show ALL activities to everyone
    serializer_class = ActivitySerializer
    permission_classes = [AllowAny]  # Anyone can list/create

    def perform_create(self, serializer):
        serializer.save()  # No user assigned — fine for demo


class ActivityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Activity.objects.all()  # Allow access to any activity
    serializer_class = ActivitySerializer
    permission_classes = [AllowAny]  # Anyone can retrieve/update/delete


class StatsView(APIView):
    permission_classes = [AllowAny]  # Anyone can view stats for demo

    def get(self, request):
        activities = Activity.objects.all()  # Change to .filter(user=request.user) later
        total_distance = activities.aggregate(Sum('distance_km'))['distance_km__sum'] or 0
        total_duration = activities.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
        total_activities = activities.count()

        # Example goal progress (customize as needed)
        goal_distance = 100  # Hardcoded goal in km - make dynamic if you add a Goal model
        progress_percentage = (total_distance / goal_distance * 100) if goal_distance > 0 else 0

        # Pie chart data (group by type)
        activity_types = activities.values('type').annotate(count=Count('type'))

        stats = {
            'total_distance': total_distance,
            'total_duration': total_duration,
            'total_activities': total_activities,
            'progress_percentage': progress_percentage,
            'activity_types': list(activity_types)  # List for JSON serialization
        }
        return Response(stats)


# NEW: Profile View + Serializer
class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id', 'username']

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user