"""
Tests for user-related endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from users.models import UserProfile

pytestmark = pytest.mark.django_db

def test_user_profile_retrieve(authenticated_client, test_user):
    """Test retrieving user profile."""
    url = reverse('userprofile-detail', kwargs={'pk': test_user.userprofile.id})
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['email'] == test_user.email
    assert response.data['role'] == 'student'

def test_user_profile_update(authenticated_client, test_user):
    """Test updating user profile."""
    url = reverse('userprofile-detail', kwargs={'pk': test_user.userprofile.id})
    data = {
        'role': 'teacher',
        'email': test_user.email,  # Required field
        'supabase_id': str(test_user.supabase_id)  # Required field
    }
    response = authenticated_client.patch(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['role'] == 'teacher'
    
    # Verify the change in database
    test_user.userprofile.refresh_from_db()
    assert test_user.userprofile.role == 'teacher'

def test_user_profile_list_admin_only(authenticated_client, admin_client):
    """Test that only admins can list all user profiles."""
    # Regular user should not be able to list all profiles
    url = reverse('userprofile-list')
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Admin should be able to list all profiles
    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.data, list)

def test_user_profile_create_admin_only(authenticated_client, admin_client):
    """Test that only admins can create new user profiles."""
    url = reverse('userprofile-list')
    data = {
        'email': 'newuser@example.com',
        'role': 'student',
        'supabase_id': 'test-supabase-id'
    }
    
    # Regular user should not be able to create profiles
    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Admin should be able to create profiles
    response = admin_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['email'] == data['email']
    assert response.data['role'] == data['role'] 