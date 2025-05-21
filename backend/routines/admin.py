from django.contrib import admin
from .models import (
    Routine, Exercise, ClientInstructorRelationship,
    BreathingExercise, MeditationSession, CombinedRoutine,
    MediaAsset, ExerciseProgress, Achievement, ClientAchievement,
    UploadProgress
)

@admin.register(Routine)
class RoutineAdmin(admin.ModelAdmin):
    list_display = ("name", "instructor", "is_active", "created_at")
    search_fields = ("name", "instructor__email")
    list_filter = ("is_active",)

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "routine", "order")
    search_fields = ("name", "routine__name")
    list_filter = ("routine",)

@admin.register(ClientInstructorRelationship)
class ClientInstructorRelationshipAdmin(admin.ModelAdmin):
    list_display = ("client", "instructor", "created_at")
    search_fields = ("client__email", "instructor__email")
    list_filter = ("instructor",)

@admin.register(BreathingExercise)
class BreathingExerciseAdmin(admin.ModelAdmin):
    list_display = ("name", "instructor", "pattern_type", "difficulty_level", "is_active")
    search_fields = ("name", "instructor__email")
    list_filter = ("pattern_type", "difficulty_level", "is_active")

@admin.register(MeditationSession)
class MeditationSessionAdmin(admin.ModelAdmin):
    list_display = ("name", "instructor", "session_type", "duration_minutes", "difficulty_level", "is_active")
    search_fields = ("name", "instructor__email")
    list_filter = ("session_type", "difficulty_level", "is_active")

@admin.register(CombinedRoutine)
class CombinedRoutineAdmin(admin.ModelAdmin):
    list_display = ("name", "instructor", "is_active", "created_at")
    search_fields = ("name", "instructor__email")
    list_filter = ("is_active",)

@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    list_display = ("name", "asset_type", "file_size", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("asset_type", "is_active")

@admin.register(ExerciseProgress)
class ExerciseProgressAdmin(admin.ModelAdmin):
    list_display = ("client", "exercise", "breathing_exercise", "meditation_session", "completed_at", "duration_seconds")
    search_fields = ("client__email", "exercise__name", "breathing_exercise__name", "meditation_session__name")
    list_filter = ("completed_at",)

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ("name", "achievement_type", "is_active")
    search_fields = ("name",)
    list_filter = ("achievement_type", "is_active")

@admin.register(ClientAchievement)
class ClientAchievementAdmin(admin.ModelAdmin):
    list_display = ("client", "achievement", "earned_at")
    search_fields = ("client__email", "achievement__name")
    list_filter = ("earned_at",)

@admin.register(UploadProgress)
class UploadProgressAdmin(admin.ModelAdmin):
    list_display = ("file_name", "asset_type", "status", "progress", "created_at")
    search_fields = ("file_name",)
    list_filter = ("status", "asset_type") 