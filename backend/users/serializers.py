from rest_framework import serializers
from .models import UserProfile
from django.core.validators import MinLengthValidator, RegexValidator

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[MinLengthValidator(8)],
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = UserProfile
        fields = ['email', 'password', 'confirm_password', 'full_name', 'role']
        extra_kwargs = {
            'email': {'required': True},
            'full_name': {'required': True},
            'role': {'required': True}
        }
    
    def validate(self, data):
        """Validate that passwords match and role is valid."""
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        
        if data['role'] not in dict(UserProfile.ROLE_CHOICES):
            raise serializers.ValidationError("Invalid role selected.")
        
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile management."""
    email = serializers.EmailField(read_only=True)
    role = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'email',
            'role',
            'full_name',
            'phone',
            'preferences',
            'created_at',
            'updated_at'
        ]
        read_only_fields = [
            'id',
            'email',
            'role',
            'created_at',
            'updated_at',
            'supabase_id'
        ]

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    phone = serializers.CharField(
        required=False,
        allow_blank=True,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ]
    )
    preferences = serializers.JSONField(required=False)
    
    class Meta:
        model = UserProfile
        fields = ['full_name', 'phone', 'preferences']
        extra_kwargs = {
            'full_name': {'required': False},
            'phone': {'required': False},
            'preferences': {'required': False}
        }
    
    def validate_preferences(self, value):
        """Validate preferences JSON structure."""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Preferences must be a JSON object")
        
        allowed_keys = {'notifications', 'email_updates', 'dark_mode', 'language'}
        if not all(key in allowed_keys for key in value.keys()):
            raise serializers.ValidationError(
                f"Invalid preference keys. Allowed keys: {', '.join(allowed_keys)}"
            )
        
        return value 