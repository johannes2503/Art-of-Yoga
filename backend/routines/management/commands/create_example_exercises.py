from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from routines.models import BreathingExercise, MeditationSession, MediaAsset
from users.models import UserProfile
import uuid

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates example breathing exercises and meditation sessions'

    def handle(self, *args, **kwargs):
        # Create an instructor if none exists
        instructor, created = UserProfile.objects.get_or_create(
            email='instructor@example.com',
            defaults={
                'role': 'instructor',
                'full_name': 'Example Instructor',
                'supabase_id': uuid.uuid4()  # Generate a random UUID for the example
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created example instructor'))

        # Example Breathing Exercise: Box Breathing
        box_breathing, created = BreathingExercise.objects.get_or_create(
            name='Box Breathing',
            instructor=instructor,
            defaults={
                'description': 'A calming breathing technique that helps reduce stress and anxiety by following a 4-4-4-4 pattern.',
                'pattern': {
                    'inhale': 4,
                    'hold': 4,
                    'exhale': 4,
                    'hold': 4,
                    'cycles': 5
                },
                'timer_seconds': 300,  # 5 minutes
                'difficulty_level': 'beginner',
                'focus_areas': ['Stress Relief', 'Anxiety Management', 'Focus'],
                'benefits': [
                    'Reduces stress and anxiety',
                    'Improves focus and concentration',
                    'Promotes emotional balance',
                    'Enhances respiratory function'
                ],
                'mastery_criteria': {
                    'duration': 600,  # 10 minutes
                    'cycles_completed': 10,
                    'consistency_days': 7
                },
                'progression_milestones': [
                    'Complete 5 cycles with 4-4-4-4 pattern',
                    'Extend to 10 minutes duration',
                    'Master 6-6-6-6 pattern',
                    'Practice daily for 2 weeks'
                ],
                'consistency_goals': {
                    'daily_practice': True,
                    'minimum_duration': 300,  # 5 minutes
                    'weekly_sessions': 5
                },
                'visual_cues': {
                    'shape': 'box',
                    'animation_speed': 'slow',
                    'color_transitions': True
                },
                'audio_cues': {
                    'inhale_sound': 'gentle_bell',
                    'exhale_sound': 'soft_chime',
                    'transition_sound': 'subtle_tone'
                }
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Box Breathing exercise'))

        # Example Meditation Session: Body Scan
        body_scan, created = MeditationSession.objects.get_or_create(
            name='Guided Body Scan Meditation',
            instructor=instructor,
            defaults={
                'description': 'A mindfulness meditation that guides you through a systematic scan of your body, promoting relaxation and body awareness.',
                'meditation_type': 'body_scan',
                'duration_seconds': 900,  # 15 minutes
                'difficulty_level': 'beginner',
                'script': '''
                    Begin by finding a comfortable position...
                    Take a few deep breaths to center yourself...
                    Starting at the top of your head, bring awareness to each part of your body...
                    Notice any sensations, tension, or relaxation...
                    Move slowly down through your body...
                    End with a few deep breaths and gentle movement.
                ''',
                'focus_points': [
                    'Body awareness',
                    'Physical sensations',
                    'Present moment attention',
                    'Non-judgmental observation'
                ],
                'mindfulness_prompts': [
                    'What sensations do you notice in this area?',
                    'Is there tension or relaxation?',
                    'Can you breathe into this space?',
                    'How does this part of your body feel?'
                ],
                'guided_sequence': [
                    {'time': 0, 'action': 'Introduction and settling'},
                    {'time': 60, 'action': 'Begin at head'},
                    {'time': 180, 'action': 'Move to shoulders and arms'},
                    {'time': 300, 'action': 'Focus on chest and back'},
                    {'time': 420, 'action': 'Scan abdomen and hips'},
                    {'time': 540, 'action': 'Move to legs and feet'},
                    {'time': 780, 'action': 'Full body awareness'},
                    {'time': 840, 'action': 'Closing and gentle movement'}
                ],
                'transition_points': [
                    {'time': 60, 'description': 'Moving from introduction to body scan'},
                    {'time': 780, 'description': 'Transitioning to full body awareness'},
                    {'time': 840, 'description': 'Preparing to end session'}
                ],
                'session_goals': {
                    'primary': 'Develop body awareness and relaxation',
                    'secondary': [
                        'Reduce physical tension',
                        'Improve present moment awareness',
                        'Enhance mind-body connection'
                    ]
                },
                'achievement_criteria': {
                    'completion': 'Complete full body scan',
                    'focus': 'Maintain attention on body sensations',
                    'relaxation': 'Notice areas of tension and relaxation'
                },
                'focus_level_assessment': {
                    'indicators': [
                        'Awareness of body sensations',
                        'Ability to stay present',
                        'Quality of relaxation'
                    ],
                    'rating_scale': '1-5'
                },
                'progression_path': [
                    'Master 15-minute body scan',
                    'Extend to 20-minute sessions',
                    'Add mindful movement',
                    'Incorporate into daily routine'
                ]
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS('Created Body Scan meditation session'))

        self.stdout.write(self.style.SUCCESS('Successfully created example exercises')) 