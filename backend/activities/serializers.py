from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Activity, Profile  # Add Activity if missing

# Activity Serializer (required for your views)
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'  # Or list specific fields if you prefer

# Your existing User Serializer (unchanged)
class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='profile.avatar', required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'avatar', 'date_joined']  # Added date_joined
        read_only_fields = ['id', 'username', 'date_joined']  # Make it read-only

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