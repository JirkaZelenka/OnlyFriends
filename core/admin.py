from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import (
    UserProfile, Event, EventVote, EventChecklistItem, EventItinerary,
    Photo, Album, SubAlbum, MapLocation, WeatherAlert, CalendarEntry, RecurringEvent,
    ChatMessage, Tip, Debt, UndercoverWordPair, UndercoverGame, Notification
)


# Inline for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


# Extend User Admin
class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'event_type', 'start_date', 'created_at']
    list_filter = ['event_type', 'is_recurring', 'start_date']
    search_fields = ['title', 'description', 'location']
    filter_horizontal = ['excluded_users']


@admin.register(EventVote)
class EventVoteAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'vote', 'created_at']
    list_filter = ['vote', 'created_at']


@admin.register(EventChecklistItem)
class EventChecklistItemAdmin(admin.ModelAdmin):
    list_display = ['event', 'text', 'completed', 'assigned_to']
    list_filter = ['completed', 'event']


@admin.register(EventItinerary)
class EventItineraryAdmin(admin.ModelAdmin):
    list_display = ['event', 'time', 'description', 'order']
    list_filter = ['event']


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'event', 'visibility', 'date', 'created_at']
    list_filter = ['visibility', 'event', 'created_at']
    search_fields = ['name', 'description']


@admin.register(SubAlbum)
class SubAlbumAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_album', 'created_by', 'created_at']
    list_filter = ['parent_album', 'created_at']
    search_fields = ['name']


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['user', 'album', 'sub_album', 'event', 'uploaded_at']
    list_filter = ['album', 'event', 'uploaded_at']


@admin.register(MapLocation)
class MapLocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'location_type', 'added_by', 'is_backlog', 'created_at']
    list_filter = ['location_type', 'is_backlog']


@admin.register(WeatherAlert)
class WeatherAlertAdmin(admin.ModelAdmin):
    list_display = ['alert_type', 'title', 'severity', 'active', 'created_at']
    list_filter = ['alert_type', 'severity', 'active']


@admin.register(CalendarEntry)
class CalendarEntryAdmin(admin.ModelAdmin):
    list_display = ['user', 'entry_type', 'start_date', 'end_date']
    list_filter = ['entry_type', 'start_date']


@admin.register(RecurringEvent)
class RecurringEventAdmin(admin.ModelAdmin):
    list_display = ['name', 'month', 'day', 'location']
    list_filter = ['month']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'created_at']
    list_filter = ['event', 'created_at']
    search_fields = ['message']


@admin.register(Tip)
class TipAdmin(admin.ModelAdmin):
    list_display = ['title', 'tip_type', 'user', 'created_at']
    list_filter = ['tip_type', 'created_at']


@admin.register(Debt)
class DebtAdmin(admin.ModelAdmin):
    list_display = ['payer', 'recipient', 'amount', 'settled', 'created_at']
    list_filter = ['settled', 'created_at']


@admin.register(UndercoverWordPair)
class UndercoverWordPairAdmin(admin.ModelAdmin):
    list_display = ['word1', 'word2', 'language', 'added_by']
    list_filter = ['language']


@admin.register(UndercoverGame)
class UndercoverGameAdmin(admin.ModelAdmin):
    list_display = ['created_by', 'is_active', 'created_at']
    filter_horizontal = ['word_pairs']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'title', 'read', 'created_at']
    list_filter = ['notification_type', 'read', 'created_at']

