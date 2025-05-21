"""
Pytest configuration and common fixtures for testing.
"""
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from users.models import UserProfile
import uuid

User = get_user_model()

@pytest.fixture
def api_client():
    """Return an API client instance."""
    return APIClient()

@pytest.fixture
def test_user(db):
    """Create and return a test user."""
    user = User.objects.create_user(
        email='test@example.com',
        password='testpass123',
        supabase_id=str(uuid.uuid4())
    )
    profile = UserProfile.objects.create(
        user=user,
        role='student',
        email=user.email,
        supabase_id=user.supabase_id
    )
    return user

@pytest.fixture
def authenticated_client(api_client, test_user):
    """Return an authenticated API client."""
    api_client.force_authenticate(user=test_user)
    return api_client

@pytest.fixture
def admin_user(db):
    """Create and return an admin user."""
    user = User.objects.create_user(
        email='admin@example.com',
        password='adminpass123',
        is_staff=True,
        is_superuser=True,
        supabase_id=str(uuid.uuid4())
    )
    profile = UserProfile.objects.create(
        user=user,
        role='admin',
        email=user.email,
        supabase_id=user.supabase_id
    )
    return user

@pytest.fixture
def admin_client(api_client, admin_user):
    """Return an authenticated API client with admin privileges."""
    api_client.force_authenticate(user=admin_user)
    return api_client 