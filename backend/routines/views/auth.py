from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """
    Register a new user and send verification email.
    
    Expected payload:
    {
        "email": "user@example.com",
        "password": "securepassword",
        "first_name": "John",
        "last_name": "Doe"
    }
    """
    try:
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not request.data.get(field):
                return Response(
                    {'error': f'{field} is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Check if user already exists
        if User.objects.filter(email=request.data['email']).exists():
            return Response(
                {'error': 'User with this email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate password
        try:
            validate_password(request.data['password'])
        except ValidationError as e:
            return Response(
                {'error': e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create user (initially inactive)
        user = User.objects.create_user(
            email=request.data['email'],
            password=request.data['password'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            is_active=False  # User needs to verify email
        )

        # Generate verification token
        token = get_random_string(length=32)
        token_expiry = timezone.now() + timedelta(hours=24)

        # Store token in session
        request.session[f'email_verification_token_{user.id}'] = {
            'token': token,
            'expiry': token_expiry
        }

        # Generate verification link
        verification_link = f"{settings.FRONTEND_URL}/verify-email?token={token}&email={user.email}"

        # Send verification email
        try:
            send_mail(
                'Verify Your Email Address',
                f'Click the following link to verify your email address: {verification_link}\n\n'
                f'This link will expire in 24 hours.\n\n'
                f'If you did not create this account, please ignore this email.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            # If email sending fails, delete the user and return error
            user.delete()
            return Response(
                {'error': 'Failed to send verification email. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            'message': 'Registration successful. Please check your email to verify your account.',
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """
    Authenticate a user and return JWT tokens.
    
    Expected payload:
    {
        "email": "user@example.com",
        "password": "securepassword"
    }
    """
    try:
        # Validate required fields
        if not request.data.get('email') or not request.data.get('password'):
            return Response(
                {'error': 'Both email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get user
        try:
            user = User.objects.get(email=request.data['email'])
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Check password
        if not user.check_password(request.data['password']):
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def refresh_token(request):
    """
    Refresh the access token using a refresh token.
    
    Expected payload:
    {
        "refresh": "your.refresh.token"
    }
    """
    try:
        if not request.data.get('refresh'):
            return Response(
                {'error': 'Refresh token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            refresh = RefreshToken(request.data['refresh'])
            access_token = str(refresh.access_token)
            
            return Response({
                'access': access_token
            })
        except Exception as e:
            return Response(
                {'error': 'Invalid refresh token'},
                status=status.HTTP_401_UNAUTHORIZED
            )

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    """
    Get the authenticated user's profile information.
    """
    try:
        user = request.user
        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
        })
    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update the authenticated user's profile information.
    
    Expected payload (all fields optional):
    {
        "first_name": "John",
        "last_name": "Doe",
        "current_password": "currentpassword",  # Required if changing password
        "new_password": "newpassword"          # Optional, requires current_password
    }
    """
    try:
        user = request.user
        data = request.data

        # Update basic profile fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']

        # Handle password change if requested
        if 'new_password' in data:
            if not data.get('current_password'):
                return Response(
                    {'error': 'Current password is required to set a new password'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verify current password
            if not user.check_password(data['current_password']):
                return Response(
                    {'error': 'Current password is incorrect'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Validate new password
            try:
                validate_password(data['new_password'])
            except ValidationError as e:
                return Response(
                    {'error': e.messages},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            user.set_password(data['new_password'])

        # Save changes
        user.save()

        return Response({
            'id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined,
            'last_login': user.last_login,
        })

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    """
    Request a password reset token to be sent to the user's email.
    
    Expected payload:
    {
        "email": "user@example.com"
    }
    """
    try:
        email = request.data.get('email')
        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Return success even if user doesn't exist to prevent email enumeration
            return Response({
                'message': 'If an account exists with this email, you will receive a password reset link.'
            })

        # Generate a secure token
        token = get_random_string(length=32)
        token_expiry = timezone.now() + timedelta(hours=24)  # Token valid for 24 hours

        # Store token in user's session or a separate model
        # For now, we'll use a simple approach with user's session
        request.session[f'password_reset_token_{user.id}'] = {
            'token': token,
            'expiry': token_expiry
        }

        # Generate reset link
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={token}&email={email}"

        # Send email
        try:
            send_mail(
                'Password Reset Request',
                f'Click the following link to reset your password: {reset_link}\n\n'
                f'This link will expire in 24 hours.\n\n'
                f'If you did not request this reset, please ignore this email.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
        except Exception as e:
            return Response(
                {'error': 'Failed to send reset email. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            'message': 'If an account exists with this email, you will receive a password reset link.'
        })

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def confirm_password_reset(request):
    """
    Confirm password reset using the token sent to user's email.
    
    Expected payload:
    {
        "email": "user@example.com",
        "token": "reset_token",
        "new_password": "new_secure_password"
    }
    """
    try:
        email = request.data.get('email')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not all([email, token, new_password]):
            return Response(
                {'error': 'Email, token, and new password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid reset request'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get stored token data
        stored_token_data = request.session.get(f'password_reset_token_{user.id}')
        if not stored_token_data:
            return Response(
                {'error': 'Invalid or expired reset token'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check token expiry
        if timezone.now() > stored_token_data['expiry']:
            # Clean up expired token
            del request.session[f'password_reset_token_{user.id}']
            return Response(
                {'error': 'Reset token has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify token
        if token != stored_token_data['token']:
            return Response(
                {'error': 'Invalid reset token'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate new password
        try:
            validate_password(new_password)
        except ValidationError as e:
            return Response(
                {'error': e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update password
        user.set_password(new_password)
        user.save()

        # Clean up used token
        del request.session[f'password_reset_token_{user.id}']

        return Response({
            'message': 'Password has been reset successfully'
        })

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_email_verification(request):
    """
    Request a new email verification token to be sent to the user's email.
    """
    try:
        user = request.user
        
        # Check if email is already verified
        if user.is_active:  # Assuming is_active indicates verified email
            return Response(
                {'message': 'Email is already verified'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Generate a secure token
        token = get_random_string(length=32)
        token_expiry = timezone.now() + timedelta(hours=24)  # Token valid for 24 hours

        # Store token in session
        request.session[f'email_verification_token_{user.id}'] = {
            'token': token,
            'expiry': token_expiry
        }

        # Generate verification link
        verification_link = f"{settings.FRONTEND_URL}/verify-email?token={token}&email={user.email}"

        # Send email
        try:
            send_mail(
                'Verify Your Email Address',
                f'Click the following link to verify your email address: {verification_link}\n\n'
                f'This link will expire in 24 hours.\n\n'
                f'If you did not create this account, please ignore this email.',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            return Response(
                {'error': 'Failed to send verification email. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({
            'message': 'Verification email has been sent to your email address.'
        })

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([AllowAny])
def confirm_email_verification(request):
    """
    Confirm email verification using the token sent to user's email.
    
    Expected payload:
    {
        "email": "user@example.com",
        "token": "verification_token"
    }
    """
    try:
        email = request.data.get('email')
        token = request.data.get('token')

        if not all([email, token]):
            return Response(
                {'error': 'Email and token are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid verification request'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if already verified
        if user.is_active:
            return Response(
                {'message': 'Email is already verified'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get stored token data
        stored_token_data = request.session.get(f'email_verification_token_{user.id}')
        if not stored_token_data:
            return Response(
                {'error': 'Invalid or expired verification token'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check token expiry
        if timezone.now() > stored_token_data['expiry']:
            # Clean up expired token
            del request.session[f'email_verification_token_{user.id}']
            return Response(
                {'error': 'Verification token has expired'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify token
        if token != stored_token_data['token']:
            return Response(
                {'error': 'Invalid verification token'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Activate user account
        user.is_active = True
        user.save()

        # Clean up used token
        del request.session[f'email_verification_token_{user.id}']

        # Generate new tokens for immediate login
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'Email has been verified successfully',
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """
    Logout the user by blacklisting their refresh token.
    
    Expected payload:
    {
        "refresh": "your.refresh.token"  # Optional, if not provided will blacklist all user's tokens
    }
    """
    try:
        refresh_token = request.data.get('refresh')
        
        if refresh_token:
            # Blacklist specific refresh token
            try:
                token = OutstandingToken.objects.get(token=refresh_token)
                BlacklistedToken.objects.get_or_create(token=token)
            except OutstandingToken.DoesNotExist:
                return Response(
                    {'error': 'Invalid refresh token'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            # Blacklist all refresh tokens for the user
            tokens = OutstandingToken.objects.filter(user_id=request.user.id)
            for token in tokens:
                BlacklistedToken.objects.get_or_create(token=token)

        return Response({
            'message': 'Successfully logged out'
        })

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        ) 