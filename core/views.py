from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms
from datetime import date
from .models import (
    Event, Photo, Album, SubAlbum, MapLocation, WeatherAlert, CalendarEntry, RecurringEvent,
    ChatMessage, Tip, Debt, UndercoverWordPair, UndercoverGame, Notification,
    EventVote, EventChecklistItem, EventItinerary
)
from .forms import (
    EventForm, PhotoForm, AlbumForm, SubAlbumForm, MapLocationForm, CalendarEntryForm, RecurringEventForm,
    ChatMessageForm, TipForm, DebtForm, UndercoverWordPairForm,
    EventChecklistItemForm, EventItineraryForm
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
def event_create(request):
    """Create a new event"""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            form.save_m2m()  # Save many-to-many relationships
            messages.success(request, 'Událost byla úspěšně vytvořena!')
            return redirect('core:event_detail', event_id=event.id)
    else:
        form = EventForm()
    return render(request, 'core/event_form.html', {'form': form, 'title': 'Nová událost'})


@login_required
def event_edit(request, event_id):
    """Edit an existing event"""
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Událost byla úspěšně upravena!')
            return redirect('core:event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'core/event_form.html', {'form': form, 'event': event, 'title': 'Upravit událost'})


@login_required
def event_delete(request, event_id):
    """Delete an event (with confirmation)"""
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Událost byla smazána.')
        return redirect('core:events_list')
    return render(request, 'core/event_confirm_delete.html', {'event': event})


@login_required
def event_detail(request, event_id):
    """Event detail page with voting, checklist, chat, itinerary"""
    event = get_object_or_404(Event, id=event_id)
    
    # Handle voting
    if request.method == 'POST' and 'vote' in request.POST:
        vote_value = request.POST.get('vote') == 'true'
        EventVote.objects.update_or_create(
            event=event,
            user=request.user,
            defaults={'vote': vote_value}
        )
        messages.success(request, 'Váš hlas byl zaznamenán!')
        return redirect('core:event_detail', event_id=event.id)
    
    # Handle checklist item creation
    if request.method == 'POST' and 'checklist_text' in request.POST:
        checklist_form = EventChecklistItemForm(request.POST)
        if checklist_form.is_valid():
            item = checklist_form.save(commit=False)
            item.event = event
            item.save()
            messages.success(request, 'Položka byla přidána do checklistu!')
            return redirect('core:event_detail', event_id=event.id)
    
    # Handle itinerary item creation
    if request.method == 'POST' and 'itinerary_description' in request.POST:
        itinerary_form = EventItineraryForm(request.POST)
        if itinerary_form.is_valid():
            item = itinerary_form.save(commit=False)
            item.event = event
            item.save()
            messages.success(request, 'Položka byla přidána do itineráře!')
            return redirect('core:event_detail', event_id=event.id)
    
    # Handle chat message
    if request.method == 'POST' and 'chat_message' in request.POST:
        message_text = request.POST.get('chat_message')
        if message_text:
            ChatMessage.objects.create(
                user=request.user,
                event=event,
                message=message_text
            )
            messages.success(request, 'Zpráva byla odeslána!')
            return redirect('core:event_detail', event_id=event.id)
    
    # Get user's vote
    user_vote = None
    try:
        vote = EventVote.objects.get(event=event, user=request.user)
        user_vote = vote.vote
    except EventVote.DoesNotExist:
        pass
    
    # Get albums for this event
    albums = Album.objects.filter(event=event)
    visible_albums = [album for album in albums if album.can_view(request.user)]
    
    # Check if event has photos
    has_photos = Photo.objects.filter(event=event).exists() or albums.exists()
    
    checklist_form = EventChecklistItemForm()
    itinerary_form = EventItineraryForm()
    
    return render(request, 'core/event_detail.html', {
        'event': event,
        'user_vote': user_vote,
        'checklist_form': checklist_form,
        'itinerary_form': itinerary_form,
        'albums': visible_albums,
        'has_photos': has_photos,
    })


@login_required
def photos_list(request):
    """Photo gallery with albums"""
    # Get albums user can view
    all_albums = Album.objects.all()
    visible_albums = [album for album in all_albums if album.can_view(request.user)]
    
    # Get standalone photos (not in albums)
    standalone_photos = Photo.objects.filter(album=None).order_by('-uploaded_at')
    
    return render(request, 'core/photos_list.html', {
        'albums': visible_albums,
        'standalone_photos': standalone_photos
    })


@login_required
def album_detail(request, album_id):
    """Album detail page with photos and sub-albums"""
    album = get_object_or_404(Album, id=album_id)
    
    # Check if user can view
    if not album.can_view(request.user):
        messages.error(request, 'Nemáte oprávnění zobrazit toto album.')
        return redirect('core:photos_list')
    
    # Get photos in this album (not in sub-albums)
    photos = album.photos.filter(sub_album=None).order_by('-uploaded_at')
    sub_albums = album.sub_albums.all()
    
    return render(request, 'core/album_detail.html', {
        'album': album,
        'photos': photos,
        'sub_albums': sub_albums
    })


@login_required
def sub_album_detail(request, sub_album_id):
    """Sub-album detail page"""
    sub_album = get_object_or_404(SubAlbum, id=sub_album_id)
    
    # Check if user can view parent album
    if not sub_album.parent_album.can_view(request.user):
        messages.error(request, 'Nemáte oprávnění zobrazit toto sub-album.')
        return redirect('core:photos_list')
    
    photos = sub_album.photos.all().order_by('-uploaded_at')
    
    return render(request, 'core/sub_album_detail.html', {
        'sub_album': sub_album,
        'photos': photos
    })


@login_required
def album_create(request, event_id=None):
    """Create a new album"""
    event = None
    if event_id:
        event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.save(commit=False)
            album.owner = request.user
            # If event is provided and date is not set, use event start date
            if event and not album.date and event.start_date:
                album.date = event.start_date.date()
            album.save()
            messages.success(request, 'Album bylo úspěšně vytvořeno!')
            return redirect('core:album_detail', album_id=album.id)
    else:
        initial = {}
        if event:
            initial['event'] = event.id
            # Prefill date from event start date
            if event.start_date:
                initial['date'] = event.start_date.date()
        form = AlbumForm(initial=initial)
    
    return render(request, 'core/album_form.html', {'form': form, 'title': 'Nové album', 'event': event})


@login_required
def album_edit(request, album_id):
    """Edit an album"""
    album = get_object_or_404(Album, id=album_id)
    
    # Only owner can edit
    if album.owner != request.user:
        messages.error(request, 'Můžete upravovat pouze vlastní alba.')
        return redirect('core:album_detail', album_id=album.id)
    
    if request.method == 'POST':
        form = AlbumForm(request.POST, request.FILES, instance=album)
        if form.is_valid():
            form.save()
            messages.success(request, 'Album bylo upraveno!')
            return redirect('core:album_detail', album_id=album.id)
    else:
        form = AlbumForm(instance=album)
    return render(request, 'core/album_form.html', {'form': form, 'album': album, 'title': 'Upravit album'})


@login_required
def sub_album_create(request, album_id):
    """Create a sub-album within an album"""
    album = get_object_or_404(Album, id=album_id)
    
    # Check if user can view the album
    if not album.can_view(request.user):
        messages.error(request, 'Nemáte oprávnění vytvořit sub-album v tomto albu.')
        return redirect('core:photos_list')
    
    if request.method == 'POST':
        form = SubAlbumForm(request.POST)
        if form.is_valid():
            sub_album = form.save(commit=False)
            sub_album.parent_album = album
            sub_album.created_by = request.user
            sub_album.save()
            messages.success(request, 'Sub-album bylo vytvořeno!')
            return redirect('core:album_detail', album_id=album.id)
    else:
        form = SubAlbumForm()
    return render(request, 'core/sub_album_form.html', {'form': form, 'album': album, 'title': 'Nový sub-album'})


@login_required
def photo_create(request, album_id=None, sub_album_id=None):
    """Add a new photo"""
    album = None
    sub_album = None
    redirect_url = 'core:photos_list'
    
    if album_id:
        album = get_object_or_404(Album, id=album_id)
        if not album.can_view(request.user):
            messages.error(request, 'Nemáte oprávnění přidat foto do tohoto alba.')
            return redirect('core:photos_list')
        redirect_url = 'core:album_detail'
        redirect_id = album.id
    elif sub_album_id:
        sub_album = get_object_or_404(SubAlbum, id=sub_album_id)
        if not sub_album.parent_album.can_view(request.user):
            messages.error(request, 'Nemáte oprávnění přidat foto do tohoto sub-alba.')
            return redirect('core:photos_list')
        album = sub_album.parent_album
        redirect_url = 'core:sub_album_detail'
        redirect_id = sub_album.id
    
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            if album:
                photo.album = album
            if sub_album:
                photo.sub_album = sub_album
            photo.save()
            messages.success(request, 'Foto bylo úspěšně přidáno!')
            if sub_album:
                return redirect('core:sub_album_detail', sub_album_id=sub_album.id)
            elif album:
                return redirect('core:album_detail', album_id=album.id)
            return redirect('core:photos_list')
    else:
        initial = {}
        if album:
            initial['album'] = album
        if sub_album:
            initial['sub_album'] = sub_album
        form = PhotoForm(initial=initial)
    
    return render(request, 'core/photo_form.html', {
        'form': form, 
        'title': 'Přidat foto',
        'album': album,
        'sub_album': sub_album
    })


@login_required
def photo_edit(request, photo_id):
    """Edit a photo"""
    photo = get_object_or_404(Photo, id=photo_id)
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Foto bylo upraveno!')
            return redirect('core:photos_list')
    else:
        form = PhotoForm(instance=photo)
    return render(request, 'core/photo_form.html', {'form': form, 'photo': photo, 'title': 'Upravit foto'})


@login_required
def maps_list(request):
    """Maps for planning trips"""
    locations = MapLocation.objects.all()
    return render(request, 'core/maps_list.html', {'locations': locations})


@login_required
def map_create(request):
    """Add a new map location"""
    if request.method == 'POST':
        form = MapLocationForm(request.POST)
        if form.is_valid():
            location = form.save(commit=False)
            location.added_by = request.user
            location.save()
            messages.success(request, 'Místo bylo přidáno!')
            return redirect('core:maps_list')
    else:
        form = MapLocationForm()
    return render(request, 'core/map_form.html', {'form': form, 'title': 'Přidat místo'})


@login_required
def map_edit(request, location_id):
    """Edit a map location"""
    location = get_object_or_404(MapLocation, id=location_id)
    if request.method == 'POST':
        form = MapLocationForm(request.POST, instance=location)
        if form.is_valid():
            form.save()
            messages.success(request, 'Místo bylo upraveno!')
            return redirect('core:maps_list')
    else:
        form = MapLocationForm(instance=location)
    return render(request, 'core/map_form.html', {'form': form, 'location': location, 'title': 'Upravit místo'})


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
def calendar_entry_create(request):
    """Add a calendar entry"""
    if request.method == 'POST':
        form = CalendarEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            messages.success(request, 'Záznam byl přidán do kalendáře!')
            return redirect('core:calendar_view')
    else:
        form = CalendarEntryForm()
    return render(request, 'core/calendar_form.html', {'form': form, 'title': 'Přidat záznam'})


@login_required
def calendar_entry_edit(request, entry_id):
    """Edit a calendar entry"""
    entry = get_object_or_404(CalendarEntry, id=entry_id)
    if request.method == 'POST':
        form = CalendarEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            messages.success(request, 'Záznam byl upraven!')
            return redirect('core:calendar_view')
    else:
        form = CalendarEntryForm(instance=entry)
    return render(request, 'core/calendar_form.html', {'form': form, 'entry': entry, 'title': 'Upravit záznam'})


@login_required
def recurring_events(request):
    """Regular annual events"""
    events = RecurringEvent.objects.all().order_by('month', 'day')
    return render(request, 'core/recurring_events.html', {'events': events})


@login_required
def recurring_event_create(request):
    """Add a recurring event"""
    if request.method == 'POST':
        form = RecurringEventForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pravidelná akce byla přidána!')
            return redirect('core:recurring_events')
    else:
        form = RecurringEventForm()
    return render(request, 'core/recurring_event_form.html', {'form': form, 'title': 'Přidat pravidelnou akci'})


@login_required
def recurring_event_edit(request, event_id):
    """Edit a recurring event"""
    event = get_object_or_404(RecurringEvent, id=event_id)
    if request.method == 'POST':
        form = RecurringEventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pravidelná akce byla upravena!')
            return redirect('core:recurring_events')
    else:
        form = RecurringEventForm(instance=event)
    return render(request, 'core/recurring_event_form.html', {'form': form, 'event': event, 'title': 'Upravit pravidelnou akci'})


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
    chat_messages = ChatMessage.objects.filter(event=None).order_by('-created_at')[:50]
    if request.method == 'POST':
        form = ChatMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.event = None  # General chat
            message.save()
            messages.success(request, 'Zpráva byla odeslána!')
            return redirect('core:chat')
    else:
        form = ChatMessageForm()
        if 'event' in form.fields:
            form.fields['event'].widget = forms.HiddenInput()  # Hide event field for general chat
    return render(request, 'core/chat.html', {'messages': chat_messages, 'form': form})


@login_required
def tips_list(request):
    """Tips for trips/restaurants/places"""
    tips = Tip.objects.all().order_by('-created_at')
    return render(request, 'core/tips_list.html', {'tips': tips})


@login_required
def tip_create(request):
    """Add a new tip"""
    if request.method == 'POST':
        form = TipForm(request.POST)
        if form.is_valid():
            tip = form.save(commit=False)
            tip.user = request.user
            tip.save()
            messages.success(request, 'Tip byl přidán!')
            return redirect('core:tips_list')
    else:
        form = TipForm()
    return render(request, 'core/tip_form.html', {'form': form, 'title': 'Přidat tip'})


@login_required
def tip_edit(request, tip_id):
    """Edit a tip"""
    tip = get_object_or_404(Tip, id=tip_id)
    if request.method == 'POST':
        form = TipForm(request.POST, instance=tip)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tip byl upraven!')
            return redirect('core:tips_list')
    else:
        form = TipForm(instance=tip)
    return render(request, 'core/tip_form.html', {'form': form, 'tip': tip, 'title': 'Upravit tip'})


@login_required
def debts_list(request):
    """Tricount-like debt settlement"""
    debts = Debt.objects.all().order_by('-created_at')
    return render(request, 'core/debts_list.html', {'debts': debts})


@login_required
def debt_create(request):
    """Add a new debt"""
    if request.method == 'POST':
        form = DebtForm(request.POST)
        if form.is_valid():
            debt = form.save(commit=False)
            debt.payer = request.user
            debt.save()
            messages.success(request, 'Dluh byl zaznamenán!')
            return redirect('core:debts_list')
    else:
        form = DebtForm()
    return render(request, 'core/debt_form.html', {'form': form, 'title': 'Přidat dluh'})


@login_required
def debt_settle(request, debt_id):
    """Mark a debt as settled"""
    debt = get_object_or_404(Debt, id=debt_id)
    if request.method == 'POST':
        debt.settled = True
        from django.utils import timezone
        debt.settled_at = timezone.now()
        debt.save()
        messages.success(request, 'Dluh byl označen jako vyrovnaný!')
        return redirect('core:debts_list')
    return render(request, 'core/debt_settle.html', {'debt': debt})


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
def undercover_wordpair_create(request):
    """Add a word pair"""
    if request.method == 'POST':
        form = UndercoverWordPairForm(request.POST)
        if form.is_valid():
            word_pair = form.save(commit=False)
            word_pair.added_by = request.user
            word_pair.save()
            messages.success(request, 'Dvojice slov byla přidána!')
            return redirect('core:undercover')
    else:
        form = UndercoverWordPairForm()
    return render(request, 'core/undercover_form.html', {'form': form, 'title': 'Přidat dvojici slov'})


@login_required
def notifications(request):
    """User notifications"""
    user_notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/notifications.html', {'notifications': user_notifications})

