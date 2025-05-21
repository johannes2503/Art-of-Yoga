from django.db import models
from django.conf import settings
from typing import Any, Dict
import json

class UserProfile(models.Model):
    """Profile for users authenticated via Supabase. Stores role and extra info."""
    supabase_id = models.UUIDField(unique=True, db_index=True, help_text="Supabase user UUID")
    email = models.EmailField(unique=True)
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("instructor", "Instructor"),
        ("client", "Client"),
    ]
    role = models.CharField(max_length=32, choices=ROLE_CHOICES, default="client")
    full_name = models.CharField(max_length=128, blank=True)
    phone = models.CharField(max_length=20, blank=True, help_text="Phone number in international format")
    preferences = models.JSONField(
        default=dict,
        help_text="User preferences (notifications, email updates, etc.)"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        """String representation."""
        return f"{self.email} ({self.role})"
    
    def get_preferences(self) -> Dict[str, Any]:
        """Get user preferences with defaults."""
        default_preferences = {
            'notifications': True,
            'email_updates': True,
            'dark_mode': False,
            'language': 'en'
        }
        return {**default_preferences, **self.preferences}
    
    def update_preferences(self, new_preferences: Dict[str, Any]) -> None:
        """Update user preferences."""
        current_preferences = self.get_preferences()
        current_preferences.update(new_preferences)
        self.preferences = current_preferences
        self.save(update_fields=['preferences', 'updated_at']) 