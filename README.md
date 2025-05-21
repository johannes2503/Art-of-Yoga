# Art of Yoga App

A mobile application designed to connect yoga instructors with their clients, enabling personalized yoga routines with multimedia support.

## Project Overview

The Art of Yoga App is built using:

- Frontend: Expo React Native with Tailwind CSS
- Backend: Python Django with Django REST Framework
- Database & Storage: PostgreSQL and Storage via Supabase

## Features

- User authentication for instructors and clients
- Multimedia support for yoga routines (images and videos)
- Breathing exercises with timer and pattern support
- Meditation sessions with audio support
- Combined routine creation and management
- Progress tracking and analytics
- Offline support
- Push notifications

## Development Setup

### Prerequisites

- Node.js (v18 or later)
- Python (v3.9 or later)
- Expo CLI
- PostgreSQL
- Supabase account

### Environment Setup

1. Clone the repository:

```bash
git clone [repository-url]
cd art_of_yoga_app
```

2. Set up environment variables:

```bash
# Backend (.env)
cp backend/.env.example backend/.env
# Frontend (.env)
cp frontend/.env.example frontend/.env
```

3. Install backend dependencies:

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

4. Install frontend dependencies:

```bash
cd frontend
npm install
```

### Running the Application

1. Start the backend server:

```bash
cd backend
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
python manage.py runserver
```

2. Start the frontend development server:

```bash
cd frontend
npm start
```

## Project Structure

```
art_of_yoga_app/
├── backend/                 # Django backend
│   ├── api/                # Django REST Framework API
│   ├── core/              # Core Django settings
│   ├── users/             # User management
│   └── routines/          # Routine management
├── frontend/              # Expo React Native frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── screens/       # App screens
│   │   ├── navigation/    # Navigation configuration
│   │   └── utils/         # Utility functions
│   └── assets/           # Static assets
└── docs/                 # Documentation
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
