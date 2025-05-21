from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .main_views import (
    RoutineViewSet,
    ClientInstructorRelationshipViewSet,
    MediaAssetViewSet,
    BreathingExerciseViewSet,
    MeditationSessionViewSet,
    CombinedRoutineViewSet,
    ExerciseProgressViewSet,
    AchievementViewSet,
    ClientAchievementViewSet,
)
from .views import auth

router = DefaultRouter()
router.register(r'routines', RoutineViewSet, basename='routine')
router.register(r'relationships', ClientInstructorRelationshipViewSet, basename='relationship')
router.register(r'media', MediaAssetViewSet, basename='media')
router.register(r'breathing-exercises', BreathingExerciseViewSet, basename='breathing-exercise')
router.register(r'meditation-sessions', MeditationSessionViewSet, basename='meditation-session')
router.register(r'combined-routines', CombinedRoutineViewSet, basename='combined-routine')
router.register(r'progress', ExerciseProgressViewSet, basename='progress')
router.register(r'achievements', AchievementViewSet, basename='achievement')
router.register(r'client-achievements', ClientAchievementViewSet, basename='client-achievement')

auth_urlpatterns = [
    path('signup/', auth.signup, name='signup'),
    path('login/', auth.login, name='login'),
    path('refresh-token/', auth.refresh_token, name='refresh-token'),
    path('profile/', auth.get_profile, name='get-profile'),
    path('profile/update/', auth.update_profile, name='update-profile'),
    path('password-reset/request/', auth.request_password_reset, name='request-password-reset'),
    path('password-reset/confirm/', auth.confirm_password_reset, name='confirm-password-reset'),
    path('email-verification/request/', auth.request_email_verification, name='request-email-verification'),
    path('email-verification/confirm/', auth.confirm_email_verification, name='confirm-email-verification'),
    path('logout/', auth.logout, name='logout'),
]

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include((auth_urlpatterns, 'auth'))),
] 