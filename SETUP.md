# Setup Instructions

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate virtual environment:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser (for admin access):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. Access the application:
- Main app: http://127.0.0.1:8000/
- Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

- `onlyfriends/` - Main Django project settings
- `core/` - Main application with all models and views
- `templates/` - HTML templates
- `static/` - Static files (CSS, JS, images)
- `media/` - User uploaded files (photos)

## Features Implemented

All 14 features from README.md are represented in the models:

1. ✅ Event cards with voting, organizer, checklist, chat, itinerary
2. ✅ Secret events (exclude users)
3. ✅ Photo sharing (images or album links)
4. ✅ Map locations for planning (Ferraty, trips, etc.)
5. ✅ Weather alerts (fire, wind, storms)
6. ✅ Calendar for availability/booked vacations
7. ✅ Recurring annual events
8. ✅ Birthdays tracking
9. ✅ General and event-specific chat
10. ✅ Tips for trips/restaurants/places
11. ✅ User preferences for notifications
12. ✅ Debt settlement (Tricount-like) with QR codes
13. ✅ Undercover game word pairs (CZ/EN)
14. ✅ Notifications system (WhatsApp/App)

## Next Steps

- Create detailed templates for each view
- Add forms for creating/editing data
- Implement authentication and authorization
- Add API endpoints if needed
- Set up WhatsApp integration for notifications
- Add payment QR code generation
- Implement Undercover game logic

