from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from django.db.models import Sum, Count
from django.contrib.auth.models import User
from .models import Activity, Profile
from .serializers import ActivitySerializer
from rest_framework import serializers
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class ActivityListCreateView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]  # Require login

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Assign to logged-in user

class ActivityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Activity.objects.filter(user=self.request.user)  # Anyone can retrieve/update/delete

class StatsView(APIView):
    permission_classes = [IsAuthenticated]  # Require login for user-specific stats

    def get(self, request):
        activities = Activity.objects.filter(user=request.user)  # User-specific
        total_distance = activities.aggregate(Sum('distance_km'))['distance_km__sum'] or 0
        total_duration = activities.aggregate(Sum('duration_minutes'))['duration_minutes__sum'] or 0
        total_activities = activities.count()
        total_calories = activities.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0

        # Example goal progress (customize as needed)
        goal_distance = 100  # Hardcoded goal in km - make dynamic if you add a Goal model
        progress_percentage = (total_distance / goal_distance * 100) if goal_distance > 0 else 0

        # Pie chart data (group by type)
        activity_types = activities.values('activity_type').annotate(count=Count('activity_type'))  # Fixed field name

        stats = {
            'total_distance': total_distance,
            'total_duration': total_duration,
            'total_activities': total_activities,
            'total_calories': total_calories,
            'progress_percentage': progress_percentage,
            'activity_types': list(activity_types)  # List for JSON serialization
        }
        return Response(stats)

# NEW: Profile View + Serializer
class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='profile.avatar', required=False)  # Made writable

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'avatar']
        read_only_fields = ['id', 'username']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if ret['avatar'] and request:
            ret['avatar'] = request.build_absolute_uri(ret['avatar'])
        return ret

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        if hasattr(instance, 'profile'):
            profile = instance.profile
        else:
            profile = Profile.objects.create(user=instance)
        if 'avatar' in profile_data:
            profile.avatar = profile_data['avatar']
            profile.save()
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        print("Received data:", self.request.data)
        print("Received files:", self.request.FILES)
        serializer.save()

# NEW: Registration View + Serializer
class RegisterSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)  # Confirmation

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Passwords must match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)