from django.core.management.base import BaseCommand
from django.conf import settings
from supabase import create_client
import json

class Command(BaseCommand):
    help = 'Set up Supabase storage buckets and policies'

    def handle(self, *args, **options):
        # Initialize Supabase client
        client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
        
        # Define buckets and their policies
        buckets = {
            'images': {
                'public': False,
                'file_size_limit': 5 * 1024 * 1024,  # 5MB
                'allowed_mime_types': ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            },
            'videos': {
                'public': False,
                'file_size_limit': 100 * 1024 * 1024,  # 100MB
                'allowed_mime_types': ['video/mp4', 'video/webm', 'video/quicktime']
            },
            'audio': {
                'public': False,
                'file_size_limit': 20 * 1024 * 1024,  # 20MB
                'allowed_mime_types': ['audio/mpeg', 'audio/wav', 'audio/ogg']
            },
            'breathing_exercises': {
                'public': False,
                'file_size_limit': 50 * 1024 * 1024,  # 50MB
                'allowed_mime_types': ['image/jpeg', 'image/png', 'video/mp4', 'audio/mpeg']
            },
            'meditation_sessions': {
                'public': False,
                'file_size_limit': 50 * 1024 * 1024,  # 50MB
                'allowed_mime_types': ['audio/mpeg', 'audio/wav', 'audio/ogg']
            },
            'combined_routines': {
                'public': False,
                'file_size_limit': 100 * 1024 * 1024,  # 100MB
                'allowed_mime_types': ['image/jpeg', 'image/png', 'video/mp4', 'audio/mpeg']
            }
        }

        # Create buckets and set up policies
        for bucket_name, config in buckets.items():
            try:
                # Create bucket if it doesn't exist
                try:
                    bucket = client.storage.get_bucket(bucket_name)
                    self.stdout.write(f"Bucket '{bucket_name}' already exists")
                except Exception:
                    bucket = client.storage.create_bucket(
                        bucket_name,
                        {'public': config['public']}
                    )
                    self.stdout.write(self.style.SUCCESS(f"Created bucket '{bucket_name}'"))

                # Set up RLS policies
                policies = [
                    # Policy for instructors to upload files
                    {
                        'name': f'{bucket_name}_instructor_upload',
                        'definition': f"""
                        (auth.role() = 'authenticated' AND 
                         EXISTS (
                           SELECT 1 FROM user_profiles 
                           WHERE supabase_id = auth.uid() 
                           AND role = 'instructor'
                         ))
                        """
                    },
                    # Policy for instructors to read their own files
                    {
                        'name': f'{bucket_name}_instructor_read',
                        'definition': f"""
                        (auth.role() = 'authenticated' AND 
                         EXISTS (
                           SELECT 1 FROM user_profiles 
                           WHERE supabase_id = auth.uid() 
                           AND role = 'instructor'
                         ) AND 
                         (storage.foldername(name))[1] = auth.uid()::text)
                        """
                    },
                    # Policy for clients to read files assigned to them
                    {
                        'name': f'{bucket_name}_client_read',
                        'definition': f"""
                        (auth.role() = 'authenticated' AND 
                         EXISTS (
                           SELECT 1 FROM user_profiles 
                           WHERE supabase_id = auth.uid() 
                           AND role = 'client'
                         ) AND 
                         EXISTS (
                           SELECT 1 FROM client_instructor_relationships 
                           WHERE client_id = auth.uid() 
                           AND instructor_id::text = (storage.foldername(name))[1]
                         ))
                        """
                    }
                ]

                # Apply policies
                for policy in policies:
                    try:
                        client.storage.from_(bucket_name).create_policy(
                            policy['name'],
                            policy['definition']
                        )
                        self.stdout.write(self.style.SUCCESS(f"Created policy '{policy['name']}' for bucket '{bucket_name}'"))
                    except Exception as e:
                        self.stdout.write(self.style.WARNING(f"Failed to create policy '{policy['name']}': {str(e)}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error setting up bucket '{bucket_name}': {str(e)}"))

        self.stdout.write(self.style.SUCCESS('Storage setup completed')) 