from django.db import models
from users.models import UserProfile
from typing import Optional
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from core.storage import SupabaseStorage
import os
import json
import uuid
from django.utils import timezone
from supabase import create_client
import time

class MediaAsset(models.Model):
    """Media asset (image, video, audio) stored in Supabase."""
    ASSET_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio')
    ]
    
    FILE_TYPE_CHOICES = {
        'image': ['image/jpeg', 'image/png', 'image/gif'],
        'video': ['video/mp4', 'video/quicktime'],
        'audio': ['audio/mpeg', 'audio/wav', 'audio/mp4']
    }
    
    MAX_FILE_SIZES = {
        'image': 10 * 1024 * 1024,  # 10MB
        'video': 100 * 1024 * 1024,  # 100MB
        'audio': 50 * 1024 * 1024   # 50MB
    }
    
    name = models.CharField(max_length=128)
    asset_type = models.CharField(max_length=16, choices=ASSET_TYPE_CHOICES)
    file = models.FileField(upload_to='media_assets/', blank=True, null=True)
    thumbnail_url = models.URLField(blank=True, default="", help_text="URL for video thumbnail or image preview")
    file_size = models.PositiveIntegerField(help_text="File size in bytes")
    duration_seconds = models.PositiveIntegerField(null=True, blank=True, help_text="Duration for video/audio in seconds")
    supabase_path = models.CharField(max_length=255, help_text="Path in Supabase storage", blank=True, null=True)
    supabase_bucket = models.CharField(max_length=64, help_text="Supabase bucket name", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def clean(self):
        """Validate file type and size."""
        if not self.file:
            return
            
        # Validate file type
        content_type = self.file.content_type
        if content_type not in self.FILE_TYPE_CHOICES.get(self.asset_type, []):
            raise ValidationError(f"Invalid file type for {self.asset_type}. Allowed types: {self.FILE_TYPE_CHOICES[self.asset_type]}")
        
        # Validate file size
        if self.file_size > self.MAX_FILE_SIZES.get(self.asset_type, 0):
            max_size_mb = self.MAX_FILE_SIZES[self.asset_type] / (1024 * 1024)
            raise ValidationError(f"File size exceeds maximum allowed size of {max_size_mb}MB for {self.asset_type}")
    
    def save(self, *args, **kwargs):
        """Handle file upload to Supabase before saving."""
        if self.file and not self.supabase_path:
            # Generate unique path
            timestamp = int(time.time())
            extension = os.path.splitext(self.file.name)[1]
            self.supabase_path = f"{self.asset_type}/{timestamp}{extension}"
            
            # Upload to Supabase
            try:
                supabase = create_client(
                    settings.SUPABASE_URL,
                    settings.SUPABASE_KEY
                )
                
                # Upload file
                with self.file.open('rb') as f:
                    supabase.storage.from_(self.supabase_bucket).upload(
                        self.supabase_path,
                        f.read(),
                        {"content-type": self.file.content_type}
                    )
                
                # Generate thumbnail for videos
                if self.asset_type == 'video' and not self.thumbnail_url:
                    # TODO: Implement video thumbnail generation
                    pass
                    
            except Exception as e:
                raise ValidationError(f"Failed to upload to Supabase: {str(e)}")
        
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        """Delete file from Supabase before deleting model."""
        if self.supabase_path:
            try:
                supabase = create_client(
                    settings.SUPABASE_URL,
                    settings.SUPABASE_KEY
                )
                supabase.storage.from_(self.supabase_bucket).remove([self.supabase_path])
            except Exception as e:
                # Log error but don't prevent deletion
                print(f"Failed to delete from Supabase: {str(e)}")
        
        super().delete(*args, **kwargs)
    
    def __str__(self) -> str:
        return f"{self.name} ({self.asset_type})"
    
    class Meta:
        ordering = ['-created_at']

class Routine(models.Model):
    """Yoga routine created by an instructor and assigned to clients."""
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    instructor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="routines")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name} (Instructor: {self.instructor.email})"

class Exercise(models.Model):
    """Exercise or pose within a routine."""
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE, related_name="exercises")
    name = models.CharField(max_length=128)
    instructions = models.TextField(blank=True)
    media_assets = models.ManyToManyField(MediaAsset, blank=True, related_name="exercises")
    order = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.name} (Routine: {self.routine.name})"

class BreathingExercise(models.Model):
    """Breathing exercise with pattern, timer, and progress tracking."""
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    instructor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="breathing_exercises")
    media_assets = models.ManyToManyField(MediaAsset, blank=True, related_name="breathing_exercises")
    
    # Breath Pattern Configuration
    inhale_duration = models.PositiveIntegerField(default=4, help_text="Duration of inhale in seconds")
    hold_duration = models.PositiveIntegerField(default=0, help_text="Duration of breath hold in seconds")
    exhale_duration = models.PositiveIntegerField(default=4, help_text="Duration of exhale in seconds")
    cycles = models.PositiveIntegerField(default=1, help_text="Number of breath cycles")
    pattern_type = models.CharField(
        max_length=32,
        choices=[
            ('equal', 'Equal Breathing'),
            ('box', 'Box Breathing'),
            ('478', '4-7-8 Breathing'),
            ('custom', 'Custom Pattern')
        ],
        default='equal'
    )
    
    # Timer Settings
    has_visual_cue = models.BooleanField(default=True)
    has_audio_cue = models.BooleanField(default=True)
    cue_style = models.CharField(
        max_length=32,
        choices=[
            ('minimal', 'Minimal'),
            ('guided', 'Guided'),
            ('nature', 'Nature Sounds')
        ],
        default='minimal'
    )
    
    # Progress Settings
    difficulty_level = models.CharField(
        max_length=16,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ],
        default='beginner'
    )
    mastery_criteria = models.JSONField(
        default=dict,
        help_text="Criteria for mastering this exercise (e.g., {'cycles_completed': 10, 'consistency_days': 7})"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name} (Instructor: {self.instructor.email})"

    def get_total_duration(self) -> int:
        """Calculate total duration of one complete cycle in seconds."""
        cycle_duration = self.inhale_duration + self.hold_duration + self.exhale_duration
        return cycle_duration * self.cycles

    class Meta:
        ordering = ['-created_at']

class MeditationSession(models.Model):
    """Meditation session with audio, script, and progress tracking."""
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    instructor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="meditation_sessions")
    
    # Session Structure
    duration_minutes = models.PositiveIntegerField(default=10, help_text="Default session duration in minutes")
    session_type = models.CharField(
        max_length=32,
        choices=[
            ('mindfulness', 'Mindfulness'),
            ('loving_kindness', 'Loving-Kindness'),
            ('body_scan', 'Body Scan'),
            ('breath_focus', 'Breath Focus'),
            ('custom', 'Custom')
        ],
        default='mindfulness'
    )
    
    # Content Management
    guided_script = models.TextField(help_text="Guided meditation script", blank=True, default="")
    focus_points = models.JSONField(
        default=list,
        help_text="List of focus points or mindfulness prompts"
    )
    background_audio = models.ForeignKey(
        MediaAsset,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="meditation_background",
        limit_choices_to={'asset_type': 'audio'}
    )
    guided_audio = models.ForeignKey(
        MediaAsset,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="meditation_guided",
        limit_choices_to={'asset_type': 'audio'}
    )
    
    # Session Settings
    has_visual_guide = models.BooleanField(default=True)
    has_ambient_sounds = models.BooleanField(default=True)
    ambient_sound_type = models.CharField(
        max_length=32,
        choices=[
            ('nature', 'Nature Sounds'),
            ('music', 'Meditation Music'),
            ('silence', 'Silence'),
            ('custom', 'Custom')
        ],
        default='nature'
    )
    
    # Progress Settings
    difficulty_level = models.CharField(
        max_length=16,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced')
        ],
        default='beginner'
    )
    focus_level_assessment = models.JSONField(
        default=dict,
        help_text="Criteria for assessing focus level during session"
    )
    achievement_criteria = models.JSONField(
        default=dict,
        help_text="Criteria for achieving mastery of this meditation"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name} (Instructor: {self.instructor.email})"

    def get_duration_seconds(self) -> int:
        """Convert duration from minutes to seconds."""
        return self.duration_minutes * 60

    class Meta:
        ordering = ['-created_at']

class CombinedRoutine(models.Model):
    """Routine that integrates yoga, breathing, and meditation exercises."""
    name = models.CharField(max_length=128)
    description = models.TextField(blank=True)
    instructor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="combined_routines")
    routines = models.ManyToManyField(Routine, blank=True, related_name="combined_routines")
    breathing_exercises = models.ManyToManyField(BreathingExercise, blank=True, related_name="combined_routines")
    meditation_sessions = models.ManyToManyField(MeditationSession, blank=True, related_name="combined_routines")
    transition_notes = models.TextField(blank=True, help_text="Instructions for transitions between exercise types")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name} (Instructor: {self.instructor.email})"

class ClientInstructorRelationship(models.Model):
    """Relationship between a client and an instructor for routine assignments."""
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="client_relationships")
    instructor = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="instructor_relationships")
    routines = models.ManyToManyField(Routine, related_name="assigned_clients", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("client", "instructor")

    def __str__(self) -> str:
        return f"Client: {self.client.email} - Instructor: {self.instructor.email}"

class ExerciseProgress(models.Model):
    """Tracks client progress for any type of exercise."""
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="exercise_progress")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="progress_tracking", null=True, blank=True)
    breathing_exercise = models.ForeignKey(BreathingExercise, on_delete=models.CASCADE, related_name="progress_tracking", null=True, blank=True)
    meditation_session = models.ForeignKey(MeditationSession, on_delete=models.CASCADE, related_name="progress_tracking", null=True, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)
    duration_seconds = models.PositiveIntegerField(help_text="Time spent on exercise in seconds")
    notes = models.TextField(blank=True)
    difficulty_rating = models.PositiveSmallIntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])
    feedback = models.TextField(blank=True)

    class Meta:
        unique_together = [
            ('client', 'exercise', 'completed_at'),
            ('client', 'breathing_exercise', 'completed_at'),
            ('client', 'meditation_session', 'completed_at'),
        ]

    def __str__(self) -> str:
        exercise_name = (
            self.exercise.name if self.exercise else
            self.breathing_exercise.name if self.breathing_exercise else
            self.meditation_session.name if self.meditation_session else
            "Unknown Exercise"
        )
        return f"{self.client.email} - {exercise_name} ({self.completed_at})"

class Achievement(models.Model):
    """Achievement system for tracking client milestones."""
    ACHIEVEMENT_TYPE_CHOICES = [
        ('consistency', 'Consistency'),
        ('mastery', 'Mastery'),
        ('milestone', 'Milestone'),
        ('special', 'Special'),
    ]
    
    name = models.CharField(max_length=128)
    description = models.TextField()
    achievement_type = models.CharField(max_length=16, choices=ACHIEVEMENT_TYPE_CHOICES)
    icon_url = models.URLField(blank=True)
    criteria = models.JSONField(help_text="Achievement criteria (e.g., {'exercise_count': 10, 'days_streak': 7})")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.achievement_type})"

class ClientAchievement(models.Model):
    """Links achievements to clients and tracks when they were earned."""
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="achievements")
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE, related_name="client_achievements")
    earned_at = models.DateTimeField(auto_now_add=True)
    progress_data = models.JSONField(default=dict, help_text="Data about how the achievement was earned")

    class Meta:
        unique_together = ('client', 'achievement')

    def __str__(self) -> str:
        return f"{self.client.email} - {self.achievement.name} ({self.earned_at})"

class UploadProgress(models.Model):
    """Tracks the progress of media file uploads."""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('uploading', 'Uploading'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed')
    ]
    
    file_name = models.CharField(max_length=255)
    asset_type = models.CharField(max_length=16, choices=MediaAsset.ASSET_TYPE_CHOICES)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default='pending')
    progress = models.PositiveIntegerField(default=0, help_text="Upload progress percentage")
    error_message = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f"{self.file_name} ({self.status})"
    
    class Meta:
        ordering = ['-created_at']
    
    @property
    def progress_percentage(self):
        """Calculate upload progress percentage."""
        return self.progress
    
    def update_progress(self, uploaded_size: int, status: str = None, error_message: str = None):
        """Update upload progress."""
        self.progress = int((uploaded_size / self.total_size) * 100) if self.total_size > 0 else 0
        if status:
            self.status = status
        if error_message:
            self.error_message = error_message
        self.save(update_fields=[
            'progress', 'status', 'error_message', 'updated_at'
        ])
    
    def to_dict(self):
        """Convert progress to dictionary."""
        return {
            'file_name': self.file_name,
            'asset_type': self.asset_type,
            'status': self.status,
            'progress_percentage': self.progress_percentage,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
    
    @classmethod
    def create_for_direct_upload(cls, policy: dict, instructor) -> 'UploadProgress':
        """Create progress tracking for direct upload."""
        return cls.objects.create(
            file_name=os.path.basename(policy['file_path']),
            asset_type=policy['asset_type'],
            total_size=policy['max_size_bytes'],
            metadata={
                'content_type': policy['content_type'],
                'bucket': policy['bucket'],
                'expires_at': policy['expires_at']
            }
        )
    
    @classmethod
    def create_for_traditional_upload(cls, file_obj, instructor, asset_type: str) -> 'UploadProgress':
        """Create progress tracking for traditional upload."""
        return cls.objects.create(
            file_name=file_obj.name,
            asset_type=asset_type,
            total_size=file_obj.size,
            metadata={
                'content_type': file_obj.content_type,
                'upload_method': 'traditional'
            }
        ) 