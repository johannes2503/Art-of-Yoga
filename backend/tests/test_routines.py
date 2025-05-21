"""
Tests for routine-related endpoints.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from routines.models import ExerciseType, Routine, RoutineExercise

pytestmark = pytest.mark.django_db

@pytest.fixture
def exercise_type(db, admin_user):
    """Create a test exercise type."""
    return ExerciseType.objects.create(
        name="Test Exercise",
        description="Test Description",
        created_by=admin_user
    )

@pytest.fixture
def routine(db, admin_user):
    """Create a test routine."""
    return Routine.objects.create(
        name="Test Routine",
        description="Test Routine Description",
        created_by=admin_user
    )

def test_exercise_type_list(authenticated_client, exercise_type):
    """Test listing exercise types."""
    url = reverse('exercisetype-list')
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == exercise_type.name

def test_exercise_type_create_admin_only(authenticated_client, admin_client):
    """Test that only admins can create exercise types."""
    url = reverse('exercisetype-list')
    data = {
        'name': 'New Exercise Type',
        'description': 'New Description'
    }
    
    # Regular user should not be able to create
    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_403_FORBIDDEN

    # Admin should be able to create
    response = admin_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == data['name']

def test_routine_create(authenticated_client):
    """Test creating a routine."""
    url = reverse('routine-list')
    data = {
        'name': 'My Routine',
        'description': 'My Routine Description'
    }
    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['name'] == data['name']
    assert response.data['created_by'] == str(authenticated_client.handler._force_user.supabase_id)

def test_routine_detail(authenticated_client, routine):
    """Test retrieving routine details."""
    url = reverse('routine-detail', kwargs={'pk': routine.id})
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == routine.name
    assert response.data['description'] == routine.description

def test_routine_update(authenticated_client, routine):
    """Test updating a routine."""
    url = reverse('routine-detail', kwargs={'pk': routine.id})
    data = {
        'name': 'Updated Routine',
        'description': 'Updated Description'
    }
    response = authenticated_client.patch(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['name'] == data['name']
    
    # Verify the change in database
    routine.refresh_from_db()
    assert routine.name == data['name']

def test_routine_exercise_management(authenticated_client, routine, exercise_type):
    """Test adding and removing exercises from a routine."""
    # Add exercise to routine
    url = reverse('routineexercise-list')
    data = {
        'routine': routine.id,
        'exercise_type': exercise_type.id,
        'order': 1,
        'duration_minutes': 10
    }
    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['routine'] == routine.id
    assert response.data['exercise_type'] == exercise_type.id

    # Verify exercise was added
    routine_exercise = RoutineExercise.objects.get(routine=routine, exercise_type=exercise_type)
    assert routine_exercise.order == 1
    assert routine_exercise.duration_minutes == 10

    # Remove exercise from routine
    url = reverse('routineexercise-detail', kwargs={'pk': routine_exercise.id})
    response = authenticated_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not RoutineExercise.objects.filter(id=routine_exercise.id).exists() 