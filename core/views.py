from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import date
from .models import (
    Event, Photo, MapLocation, WeatherAlert, CalendarEntry, RecurringEvent,
    ChatMessage, Tip, Debt, UndercoverWordPair, UndercoverGame, Notification
)


def index(request):
    """Main dashboard/home page"""
    return render(request, 'core/index.html')


@login_required
def events_list(request):
    """List of all events"""
    events = Event.objects.all().order_by('-start_date')
    return render(request, 'core/events_list.html', {'events': events})


@login_required
def event_detail(request, event_id):
    """Event detail page with voting, checklist, chat, itinerary"""
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'core/event_detail.html', {'event': event})


@login_required
def photos_list(request):
    """Photo gallery"""
    photos = Photo.objects.all().order_by('-uploaded_at')
    return render(request, 'core/photos_list.html', {'photos': photos})


@login_required
def maps_list(request):
    """Maps for planning trips"""
    locations = MapLocation.objects.all()
    return render(request, 'core/maps_list.html', {'locations': locations})


@login_required
def weather_alerts(request):
    """Weather and fire alerts"""
    alerts = WeatherAlert.objects.filter(active=True).order_by('-created_at')
    return render(request, 'core/weather_alerts.html', {'alerts': alerts})


@login_required
def calendar_view(request):
    """Calendar with availability and booked vacations"""
    entries = CalendarEntry.objects.all().order_by('start_date')
    return render(request, 'core/calendar_view.html', {'entries': entries})


@login_required
def recurring_events(request):
    """Regular annual events"""
    events = RecurringEvent.objects.all().order_by('month', 'day')
    return render(request, 'core/recurring_events.html', {'events': events})


@login_required
def birthdays(request):
    """Birthdays, especially round numbers"""
    users_with_birthdays = []
    users = User.objects.filter(profile__birthday__isnull=False)
    today = date.today()
    
    for user in users:
        if user.profile.birthday:
            age = today.year - user.profile.birthday.year - ((today.month, today.day) < (user.profile.birthday.month, user.profile.birthday.day))
            users_with_birthdays.append({
                'user': user,
                'age': age,
                'is_round': age % 10 == 0 if age > 0 else False
            })
    
    return render(request, 'core/birthdays.html', {'users_data': users_with_birthdays})


@login_required
def chat(request):
    """General chat"""
    messages = ChatMessage.objects.filter(event=None).order_by('-created_at')[:50]
    return render(request, 'core/chat.html', {'messages': messages})


@login_required
def tips_list(request):
    """Tips for trips/restaurants/places"""
    tips = Tip.objects.all().order_by('-created_at')
    return render(request, 'core/tips_list.html', {'tips': tips})


@login_required
def debts_list(request):
    """Tricount-like debt settlement"""
    debts = Debt.objects.all().order_by('-created_at')
    return render(request, 'core/debts_list.html', {'debts': debts})


@login_required
def undercover(request):
    """Undercover game word generator"""
    word_pairs = UndercoverWordPair.objects.all()
    games = UndercoverGame.objects.filter(is_active=True)
    return render(request, 'core/undercover.html', {
        'word_pairs': word_pairs,
        'games': games
    })


@login_required
def notifications(request):
    """User notifications"""
    user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/notifications.html', {'notifications': user_notifications})

