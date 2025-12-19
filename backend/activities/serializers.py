from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Activity, Profile


# Activity Serializer - FIXED: Auto-assign user, no need to send 'user' from frontend
class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = [
            'id',
            'activity_type',
            'duration',
            'distance_km',
            'calories_burned',
            'date',
            'notes',
            'created_at'
        ]
        read_only_fields = ['calories_burned', 'created_at']

    def create(self, validated_data):
        # Automatically assign the authenticated user from the request context
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        else:
            raise serializers.ValidationError("Authentication required.")
        return super().create(validated_data)


# User Serializer - Enhanced with date_joined and proper avatar handling
class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(
        source='profile.avatar',
        required=False,
        allow_null=True
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'avatar',
            'date_joined'  # For "Member Since" on profile page
        ]
        read_only_fields = ['id', 'username', 'date_joined']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')
        if ret['avatar'] and request:
            ret['avatar'] = request.build_absolute_uri(ret['avatar'])
        return ret

    def update(self, instance, validated_data):
        # Handle nested profile avatar update
        profile_data = validated_data.pop('profile', {})
        avatar = profile_data.get('avatar')

        # Update user fields
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        # Update or create profile for avatar
        profile, created = Profile.objects.get_or_create(user=instance)
        if avatar is not None:
            profile.avatar = avatar
            profile.save()

        return instance