## 1. General Setup

- [x] Set up project repository (e.g., GitHub) for version control.
- [x] Configure development environment for Expo React Native, Python Django, and Supabase.
- [ ] Set up Supabase project for PostgreSQL database and Storage.
- [x] Create initial project documentation (e.g., README, contribution guidelines).
- [x] Define environment variables for API keys, Supabase credentials, and other sensitive data.

## 2. Backend (Python Django, Django REST Framework)

- [x] Set up Django project with Django REST Framework.
- [x] Configure Django to integrate with Supabase Authentication for user management.
- [x] Create database models in Django ORM:
  - [x] User model (linked to Supabase Authentication, with role: user/instructor).
  - [x] Routine model (name, description, assigned clients, exercises/poses).
  - [x] Exercise/Pose model (name, instructions, media references).
  - [x] Client-Instructor relationship model (for routine assignments).
  - [x] Breathing Exercise model (patterns, timers, progress tracking).
  - [x] Meditation Session model (audio, scripts, progress tracking).
  - [x] Combined Routine model (exercise type integration, transitions).
- [ ] Implement RESTful API endpoints:
  - [x] Authentication: Register, login, password reset (using Supabase Authentication).
    - [x] Signup endpoint with email verification
    - [x] Login endpoint with JWT tokens
    - [x] Password reset request and confirmation
    - [x] Email verification request and confirmation
    - [x] Token refresh endpoint
    - [x] Logout endpoint with token blacklisting
    - [x] Profile management (get/update)
  - [x] User Portal: Get assigned routines, mark routines/exercises as completed.
  - [x] Instructor Portal: Create/edit/delete routines, assign routines to clients, manage client list.
  - [x] Profile: Update user/instructor profile details.
  - [ ] Media Management:
    - [ ] File upload endpoints
    - [ ] File download endpoints
    - [ ] Media metadata management
    - [ ] File validation and processing
- [ ] Set up Supabase Storage integration for uploading images (PNG, JPG) and videos (MP4).
- [ ] Implement file size validation (images ≤ 5MB, videos ≤ 50MB).
- [ ] Configure role-based access control using Supabase Row-Level Security (RLS).
- [x] Write unit tests for API endpoints and business logic.
- [ ] Deploy Django backend to a cloud platform (e.g., Heroku, Render, or AWS).

## 3. Frontend (Expo React Native, Tailwind CSS)

- [x] Initialize Expo React Native project.
- [x] Install and configure Tailwind CSS (nativewind or tailwind-rn) for styling.
- [x] Set up navigation (e.g., React Navigation) for user and instructor portals.
- [x] Implement authentication screens:
  - [x] Registration screen (email, password, name, role).
  - [x] Login screen.
  - [x] Password reset screen.
- [x] Develop user portal screens:
  - [x] Dashboard: List of assigned routines.
  - [x] Routine detail screen: Display routine name, description, exercises/poses, and media (images/videos).
  - [x] Progress tracking: Buttons to mark routines/exercises as completed.
  - [x] Profile screen: Update personal details.
- [x] Develop instructor portal screens:

  - [x] Dashboard: List of clients and their routines.
  - [x] Routine creation screen: Form for routine name, description, exercises/poses, and media uploads.
  - [x] Client management screen: Assign/unassign routines to clients.
  - [x] Routine management screen: Edit/delete routines.
  - [x] Profile screen: Update personal details.
  - [ ] Breathing exercise creation screen:
    - [ ] Timer configuration interface
    - [ ] Breath pattern designer
    - [ ] Multimedia upload for breathing exercises
    - [ ] Progress tracking setup
  - [ ] Meditation session creation screen:
    - [ ] Audio recording/upload interface
    - [ ] Session structure designer
    - [ ] Guided script editor
    - [ ] Background sound selector
  - [ ] Combined routine creation screen:
    - [ ] Exercise type mixer
    - [ ] Transition flow designer
    - [ ] Multi-type template manager
    - [ ] Client customization interface

- [x] Develop client portal screens:

  - [x] Dashboard: List of assigned routines.
  - [x] Routine detail screen: Display routine name, description, exercises/poses, and media.
  - [x] Progress tracking: Buttons to mark routines/exercises as completed.
  - [x] Profile screen: Update personal details.
  - [ ] Breathing exercise player:
    - [ ] Timer interface with visual/audio cues
    - [ ] Breath pattern visualizer
    - [ ] Progress tracking display
    - [ ] Session history viewer
  - [ ] Meditation session player:
    - [ ] Audio player with controls
    - [ ] Session progress tracker
    - [ ] Focus level assessment
    - [ ] Achievement display
  - [ ] Combined routine player:
    - [ ] Multi-type exercise navigator
    - [ ] Transition manager
    - [ ] Progress tracker
    - [ ] Achievement system

- [ ] Implement media handling:
  - [ ] Use expo-image for displaying images from Supabase Storage.
  - [ ] Use expo-av for streaming videos from Supabase Storage.
  - [ ] Audio handling:
    - [ ] Implement audio recording
    - [ ] Set up audio streaming
    - [ ] Create audio compression
    - [ ] Manage offline audio access
  - [ ] Timer system:
    - [ ] Implement countdown functionality
    - [ ] Create stopwatch feature
    - [ ] Design visual/audio cues
    - [ ] Build session tracking
- [ ] Configure Expo Push Notifications for new routine assignments.
- [x] Ensure mobile-responsive UI with Tailwind CSS for iOS and Android compatibility.
- [ ] Write unit tests for React Native components and navigation.

## 4. Database and Storage (PostgreSQL, Supabase)

- [x] Set up PostgreSQL tables in Supabase:

  - [x] Users table (linked to Supabase Authentication).
  - [x] Routines table (name, description, instructor ID, assigned client IDs).
  - [x] Exercises/Poses table (name, instructions, routine ID, media URLs).
  - [x] Client-Instructor relationships table.
  - [x] Breathing exercises table:
    - [x] Pattern configurations
    - [x] Timer settings
    - [x] Progress tracking
    - [x] Multimedia references
  - [x] Meditation sessions table:
    - [x] Audio file references
    - [x] Session structures
    - [x] Progress tracking
    - [x] Achievement data
  - [x] Combined routines table:
    - [x] Exercise type mappings
    - [x] Transition configurations
    - [x] Progress tracking
    - [x] Achievement integration

- [ ] Configure Supabase Storage buckets:
  - [ ] Images bucket (priority: high)
  - [ ] Videos bucket (priority: high)
  - [ ] Audio files bucket (priority: high)
  - [ ] Breathing exercise media bucket (priority: medium)
  - [ ] Meditation session media bucket (priority: medium)
  - [ ] Combined routine media bucket (priority: medium)
- [ ] Set up Row-Level Security (RLS) policies:
  - [x] Basic user access policies
  - [ ] Media access policies
  - [ ] Routine access policies
  - [ ] Client-instructor relationship policies
- [x] Create database migrations for schema changes.
- [x] Test database performance for routine retrieval and media access.

## 5. Security

- [ ] Enable HTTPS for all API communications.
- [x] Implement JWT token handling in Django and React Native for secure sessions.
- [ ] Secure Supabase Storage with public URLs only for authorized media access.
- [x] Validate all user inputs to prevent injection attacks.
- [x] Ensure no sensitive data (e.g., API keys) is hardcoded.

## 6. Testing and Quality Assurance

- [x] Test authentication flows (register, login, password reset).
  - [x] Email verification flow
  - [x] Password reset flow
  - [x] Token refresh flow
  - [x] Profile update flow
- [x] Test user portal functionality (view routines, mark progress, view media).
- [x] Test instructor portal functionality (create/edit/delete routines, assign clients).
- [ ] Perform cross-platform testing on iOS and Android via Expo.
- [ ] Conduct performance testing for media streaming and API response times.
- [ ] Test edge cases (e.g., large file uploads, invalid inputs).

## 7. Deployment

- [ ] Deploy Supabase project (PostgreSQL and Storage).
- [ ] Deploy Django backend to a cloud platform.
- [ ] Build and distribute Expo app for iOS and Android (e.g., via Expo EAS Build).
- [ ] Set up CI/CD pipeline for automated testing and deployment.
- [ ] Monitor app performance and errors post-deployment (e.g., using Supabase analytics, Sentry).

## 8. Documentation and Training

- [x] Document API endpoints (e.g., using Swagger or Postman).
- [ ] Create user guide for clients (how to use the app, view routines).
- [ ] Create instructor guide (how to create/assign routines, manage clients).
- [x] Prepare developer documentation for code maintenance.

## 9. Future Enhancements (Post-MVP)

- [ ] Plan integration with wearables (e.g., Apple Watch) for tracking.
- [ ] Design calendar integration for scheduling routines.
- [ ] Explore social features (e.g., progress sharing).
- [ ] Develop analytics dashboard for instructors.
- [ ] Advanced breathing pattern recognition
- [ ] Meditation session analytics
- [ ] AI-powered exercise recommendations
- [ ] Advanced audio processing features

## 10. Current Sprint Focus (Next Steps)

### High Priority

1. Media System Implementation:

   - [ ] Set up Supabase Storage buckets
   - [ ] Implement file upload/download system
   - [ ] Add file validation and compression
   - [ ] Create media management API endpoints
   - [ ] Build frontend media components

2. Exercise Type Implementation:

   - [ ] Complete breathing exercise system
   - [ ] Implement meditation session functionality
   - [ ] Build combined routine system
   - [ ] Add exercise type transitions

3. Timer and Audio Systems:
   - [ ] Implement countdown timer
   - [ ] Set up audio recording/streaming
   - [ ] Create visual/audio cues
   - [ ] Build session tracking

### Medium Priority

1. Security and Storage:

   - [ ] Complete RLS policies
   - [ ] Implement HTTPS
   - [ ] Secure media access
   - [ ] Add file access controls

2. Notification System:

   - [ ] Set up push notifications
   - [ ] Implement email notifications
   - [ ] Create in-app notifications
   - [ ] Add notification preferences

3. Analytics and Progress:
   - [ ] Implement engagement tracking
   - [ ] Set up effectiveness metrics
   - [ ] Create progress tracking
   - [ ] Build analytics dashboard

### Lower Priority

1. Offline Support
2. Social Features
3. Advanced Analytics
4. Wearable Integration

## 11. Blockers and Dependencies

### Current Blockers

1. Media System:

   - Blocks breathing exercises
   - Blocks meditation sessions
   - Blocks combined routines
   - Required for progress tracking

2. Timer System:

   - Required for breathing exercises
   - Required for meditation sessions
   - Blocks progress tracking

3. Audio System:
   - Required for meditation sessions
   - Required for combined routines
   - Blocks progress tracking

### Dependencies

1. Supabase Storage setup required for:

   - Media upload/download
   - Audio streaming
   - Progress tracking
   - Offline support

2. RLS Policies required for:

   - Media access
   - Routine access
   - Client-instructor relationships
   - Progress tracking

3. Notification System requires:
   - Push notification setup
   - Email service integration
   - In-app notification storage
   - User preferences storage
