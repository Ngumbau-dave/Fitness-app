# FitTrack - Fitness Tracker app
# FitTrack – Fitness Tracker App

Track runs, swims, etc. with Django REST API + simple HTML/JS frontend.

## Backend Setup
```bash
cd backend
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # e.g., Username: testuser, Password: testpass123
python manage.py runserver
