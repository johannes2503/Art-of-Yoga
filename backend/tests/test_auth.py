"""
Tests for authentication-related endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = pytest.mark.django_db

def test_auth_test_endpoint_unauthorized(api_client):
    """Test that unauthenticated users cannot access the auth test endpoint."""
    url = reverse('auth-test')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_auth_test_endpoint_authorized(authenticated_client):
    """Test that authenticated users can access the auth test endpoint."""
    url = reverse('auth-test')
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'message' in response.data
    assert 'user' in response.data
    assert response.data['user']['email'] == 'test@example.com'
    assert response.data['user']['role'] == 'student'
    assert 'supabase_id' in response.data['user'] 