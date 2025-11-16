from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile with preferences and QR code for payments"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    birthday = models.DateField(null=True, blank=True)
    qr_code = models.CharField(max_length=500, blank=True, help_text="QR code for payment generation")
    
    # Notification preferences
    notify_events = models.BooleanField(default=True)
    notify_birthdays = models.BooleanField(default=True)
    notify_weather_alerts = models.BooleanField(default=True)
    notify_whatsapp = models.BooleanField(default=False)
    notify_app = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} Profile"


class Event(models.Model):
    """Event card with description, location, voting, organizer, checklist, chat, itinerary"""
    EVENT_TYPES = [
        ('public', 'Public'),
        ('secret', 'Secret'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200, blank=True)
    map_location = models.ForeignKey('MapLocation', on_delete=models.SET_NULL, null=True, blank=True, related_name='events', help_text="Link to a predefined place on the map")
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES, default='public')
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='organized_events')
    
    # Date and time
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    # Secret event - excluded users
    excluded_users = models.ManyToManyField(User, blank=True, related_name='excluded_from_events')
    
    # Recurring event
    is_recurring = models.BooleanField(default=False)
    recurring_pattern = models.CharField(max_length=100, blank=True, help_text="e.g., 'yearly', 'monthly'")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title


class EventVote(models.Model):
    """Voting for events"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.BooleanField(default=True)  # True = attending, False = not attending
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'user']
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class EventChecklistItem(models.Model):
    """Checklist items for events"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='checklist_items')
    text = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.event.title} - {self.text}"


class EventItinerary(models.Model):
    """Itinerary items for events"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='itinerary_items')
    time = models.TimeField(null=True, blank=True)
    description = models.CharField(max_length=200)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'time']
    
    def __str__(self):
        return f"{self.event.title} - {self.description}"


class Album(models.Model):
    """Photo album with intro photo, date, description, and visibility settings"""
    VISIBILITY_CHOICES = [
        ('event_attendees', 'Pouze účastníci akce'),
        ('all_users', 'Všichni uživatelé'),
        ('private', 'Soukromé (pouze vlastník)'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    intro_photo = models.ImageField(upload_to='albums/intro/', blank=True, null=True, help_text="Úvodní/obálková fotka")
    date = models.DateField(null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, related_name='albums')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_albums')
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='event_attendees')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-created_at']
    
    def __str__(self):
        return self.name
    
    def can_view(self, user):
        """Check if user can view this album"""
        if self.owner == user:
            return True
        if self.visibility == 'all_users':
            return True
        if self.visibility == 'private':
            return False
        if self.visibility == 'event_attendees' and self.event:
            # Check if user attended the event
            return EventVote.objects.filter(event=self.event, user=user, vote=True).exists()
        return False


class SubAlbum(models.Model):
    """Sub-album within an album, named by the user who created it"""
    parent_album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='sub_albums')
    name = models.CharField(max_length=200, help_text="Název sub-alba (např. jméno uživatele)")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_sub_albums')
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"{self.name} ({self.parent_album.name})"


class Photo(models.Model):
    """Photos from events - can be in albums or standalone"""
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='photos', null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photos', null=True, blank=True)
    sub_album = models.ForeignKey(SubAlbum, on_delete=models.CASCADE, related_name='photos', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_photos')
    image = models.ImageField(upload_to='photos/', blank=True, null=True)
    album_link = models.URLField(blank=True, help_text="Link to external photo album")
    caption = models.TextField(blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        if self.album:
            return f"Photo by {self.user.username} - {self.album.name}"
        return f"Photo by {self.user.username} - {self.event.title if self.event else 'General'}"
    
    def get_like_count(self):
        """Get the number of likes for this photo"""
        return self.likes.count()
    
    def is_liked_by(self, user):
        """Check if a user has liked this photo"""
        if not user or not user.is_authenticated:
            return False
        return self.likes.filter(user=user).exists()


class PhotoLike(models.Model):
    """Likes for photos"""
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='photo_likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['photo', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} likes {self.photo.id}"


class MapLocation(models.Model):
    """Maps for planning trips, saving to backlog (e.g., Ferraty)"""
    LOCATION_TYPES = [
        ('ferrata', 'Ferraty'),
        ('hiking', 'Hiking'),
        ('trip', 'Trip'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    location_type = models.CharField(max_length=20, choices=LOCATION_TYPES, default='other')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_backlog = models.BooleanField(default=True, help_text="Is this in the backlog?")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class WeatherAlert(models.Model):
    """Weather and fire alerts, strong wind warnings, etc."""
    ALERT_TYPES = [
        ('fire', 'Fire Warning'),
        ('wind', 'Strong Wind'),
        ('storm', 'Storm'),
        ('other', 'Other'),
    ]
    
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    severity = models.CharField(max_length=20, default='medium')  # low, medium, high
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.alert_type} - {self.title}"


class CalendarEntry(models.Model):
    """Calendar where users can mark availability or booked vacations"""
    ENTRY_TYPES = [
        ('available', 'Available'),
        ('booked', 'Booked/Vacation'),
        ('busy', 'Busy'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calendar_entries')
    entry_type = models.CharField(max_length=20, choices=ENTRY_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.entry_type} ({self.start_date} to {self.end_date})"


class RecurringEvent(models.Model):
    """Regular annual events like 'Tři jezy', 'Povaleč' - hardcoded in calendar"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    month = models.IntegerField(help_text="Month (1-12)")
    day = models.IntegerField(help_text="Day of month")
    location = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.day}.{self.month}"


class ChatMessage(models.Model):
    """General chat messages"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    message = models.TextField()
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='chat_messages', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        event_str = f" ({self.event.title})" if self.event else ""
        return f"{self.user.username}{event_str}: {self.message[:50]}"


class Tip(models.Model):
    """Tips from users for trips/restaurants/good places"""
    TIP_TYPES = [
        ('trip', 'Trip'),
        ('restaurant', 'Restaurant'),
        ('place', 'Place'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tips')
    tip_type = models.CharField(max_length=20, choices=TIP_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200, blank=True)
    link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.get_tip_type_display()}"


class Debt(models.Model):
    """Tricount-like debt settlement"""
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paid_debts')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_debts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True, related_name='debts')
    settled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    settled_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.payer.username} owes {self.recipient.username} {self.amount}"


class UndercoverWordPair(models.Model):
    """Word pairs for Undercover game"""
    LANGUAGES = [
        ('cz', 'Czech'),
        ('en', 'English'),
    ]
    
    word1 = models.CharField(max_length=100)
    word2 = models.CharField(max_length=100)
    language = models.CharField(max_length=2, choices=LANGUAGES, default='cz')
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.word1} / {self.word2} ({self.get_language_display()})"


class UndercoverGame(models.Model):
    """Undercover game session"""
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    word_pairs = models.ManyToManyField(UndercoverWordPair)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Undercover Game by {self.created_by.username}"


class Notification(models.Model):
    """Notifications for users"""
    NOTIFICATION_TYPES = [
        ('event', 'New Event'),
        ('birthday', 'Birthday'),
        ('weather', 'Weather Alert'),
        ('message', 'New Message'),
        ('debt', 'Debt Settlement'),
        ('other', 'Other'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    read = models.BooleanField(default=False)
    sent_whatsapp = models.BooleanField(default=False)
    sent_app = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"

