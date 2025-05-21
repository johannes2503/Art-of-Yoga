from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
from django.db.models import Q
from .models import UserProfile
from .serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer
)
from .authentication import SupabaseJWTAuthentication
from .permissions import IsAdminUser, IsInstructorOrAdmin
import requests

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for user registration and profile management."""
    authentication_classes = [SupabaseJWTAuthentication]
    queryset = UserProfile.objects.all()
    
    def get_permissions(self):
        """Set permissions based on action."""
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        elif self.action in ['instructors', 'clients']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Return appropriate serializer class."""
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action in ['update', 'partial_update', 'me']:
            return UserProfileUpdateSerializer
        return UserProfileSerializer
    
    def get_queryset(self):
        """Filter queryset based on user role and action."""
        queryset = super().get_queryset()
        
        # For list action, filter based on role
        if self.action == 'list':
            if self.request.user.role == 'admin':
                return queryset
            elif self.request.user.role == 'instructor':
                # Instructors can only see their clients
                return queryset.filter(
                    role='client',
                    client_relationships__instructor=self.request.user
                )
            else:  # client
                # Clients can only see their instructors
                return queryset.filter(
                    role='instructor',
                    instructor_relationships__client=self.request.user
                )
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Handle user registration."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Create user in Supabase
        supabase_data = {
            'email': serializer.validated_data['email'],
            'password': serializer.validated_data['password'],
            'user_metadata': {
                'full_name': serializer.validated_data['full_name'],
                'role': serializer.validated_data['role']
            }
        }
        
        try:
            response = requests.post(
                f"{settings.SUPABASE_URL}/auth/v1/signup",
                json=supabase_data,
                headers={'apikey': settings.SUPABASE_KEY}
            )
            response.raise_for_status()
            supabase_user = response.json()
            
            # Create user profile in Django
            user_profile = UserProfile.objects.create(
                supabase_id=supabase_user['id'],
                email=serializer.validated_data['email'],
                full_name=serializer.validated_data['full_name'],
                role=serializer.validated_data['role']
            )
            
            return Response(
                UserProfileSerializer(user_profile).data,
                status=status.HTTP_201_CREATED
            )
            
        except requests.exceptions.RequestException as e:
            return Response(
                {'error': f'Failed to create user in Supabase: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user's profile."""
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Update current user's profile."""
        serializer = UserProfileUpdateSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserProfileSerializer(request.user).data)
    
    @action(detail=False, methods=['get'])
    def instructors(self, request):
        """Get list of instructors (for clients)."""
        if request.user.role != 'client':
            return Response(
                {'error': 'Only clients can access instructor list'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        instructors = UserProfile.objects.filter(
            role='instructor',
            instructor_relationships__client=request.user
        )
        serializer = UserProfileSerializer(instructors, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def clients(self, request):
        """Get list of clients (for instructors)."""
        if request.user.role != 'instructor':
            return Response(
                {'error': 'Only instructors can access client list'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        clients = UserProfile.objects.filter(
            role='client',
            client_relationships__instructor=request.user
        )
        serializer = UserProfileSerializer(clients, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user's password."""
        if not request.user.is_authenticated:
            return Response(
                {'error': 'Authentication required'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response(
                {'error': 'Both old and new passwords are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Update password in Supabase
            response = requests.post(
                f"{settings.SUPABASE_URL}/auth/v1/user/password",
                json={
                    'old_password': old_password,
                    'new_password': new_password
                },
                headers={
                    'apikey': settings.SUPABASE_KEY,
                    'Authorization': f"Bearer {request.auth}"
                }
            )
            response.raise_for_status()
            return Response({'message': 'Password updated successfully'})
            
        except requests.exceptions.RequestException as e:
            return Response(
                {'error': f'Failed to update password: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            ) 