from django.core.management.base import BaseCommand
from django.conf import settings
from supabase import create_client
import json

class Command(BaseCommand):
    help = 'Sets up storage buckets (policies must be set manually in Supabase dashboard)'

    def handle(self, *args, **options):
        # Initialize Supabase client
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)

        # Define bucket configurations (max 50MB per object)
        buckets = {
            'images': {
                'name': 'images',
                'public': False,
                'file_size_limit': 50 * 1024 * 1024,  # 50MB
                'allowed_mime_types': ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            },
            'videos': {
                'name': 'videos',
                'public': False,
                'file_size_limit': 50 * 1024 * 1024,  # 50MB
                'allowed_mime_types': ['video/mp4', 'video/webm', 'video/quicktime']
            },
            'audio': {
                'name': 'audio',
                'public': False,
                'file_size_limit': 20 * 1024 * 1024,  # 20MB
                'allowed_mime_types': ['audio/mpeg', 'audio/wav', 'audio/ogg']
            },
            'breathing_exercises': {
                'name': 'breathing_exercises',
                'public': False,
                'file_size_limit': 50 * 1024 * 1024,  # 50MB
                'allowed_mime_types': ['audio/mpeg', 'audio/wav', 'audio/ogg', 'video/mp4']
            },
            'meditation_sessions': {
                'name': 'meditation_sessions',
                'public': False,
                'file_size_limit': 50 * 1024 * 1024,  # 50MB
                'allowed_mime_types': ['audio/mpeg', 'audio/wav', 'audio/ogg', 'video/mp4']
            },
            'combined_routines': {
                'name': 'combined_routines',
                'public': False,
                'file_size_limit': 50 * 1024 * 1024,  # 50MB
                'allowed_mime_types': ['video/mp4', 'video/webm', 'video/quicktime']
            }
        }

        # Create buckets
        for bucket_id, config in buckets.items():
            try:
                response = supabase.storage.create_bucket(
                    id=bucket_id,
                    options={
                        'public': config['public'],
                        'file_size_limit': config['file_size_limit'],
                        'allowed_mime_types': config['allowed_mime_types']
                    }
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully created bucket: {bucket_id}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error setting up bucket \'{bucket_id}\': {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Storage setup completed.\n'))
        self.stdout.write(self.style.WARNING('NOTE: You must set up RLS (Row Level Security) policies for each bucket manually in the Supabase dashboard.')) 