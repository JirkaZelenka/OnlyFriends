from django import forms
from django.contrib.auth.models import User
from .models import (
    Event, EventVote, EventChecklistItem, EventItinerary,
    Photo, MapLocation, WeatherAlert, CalendarEntry, RecurringEvent,
    ChatMessage, Tip, Debt, UndercoverWordPair, UndercoverGame, Notification, UserProfile
)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'event_type', 'start_date', 'end_date', 
                  'is_recurring', 'recurring_pattern', 'excluded_users']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Název události'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Popis události'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Místo konání'}),
            'event_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'is_recurring': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'recurring_pattern': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'např. yearly, monthly'}),
            'excluded_users': forms.SelectMultiple(attrs={'class': 'form-control', 'size': 5}),
        }
        labels = {
            'title': 'Název',
            'description': 'Popis',
            'location': 'Místo',
            'event_type': 'Typ události',
            'start_date': 'Začátek',
            'end_date': 'Konec',
            'is_recurring': 'Pravidelná akce',
            'recurring_pattern': 'Vzor opakování',
            'excluded_users': 'Vyloučení uživatelé (pro tajné akce)',
        }


class EventVoteForm(forms.ModelForm):
    class Meta:
        model = EventVote
        fields = ['vote']
        widgets = {
            'vote': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'vote': 'Přijdu na akci',
        }


class EventChecklistItemForm(forms.ModelForm):
    class Meta:
        model = EventChecklistItem
        fields = ['text', 'completed', 'assigned_to']
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control'}),
            'completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'text': 'Text',
            'completed': 'Hotovo',
            'assigned_to': 'Přiřazeno',
        }


class EventItineraryForm(forms.ModelForm):
    class Meta:
        model = EventItinerary
        fields = ['time', 'description', 'order']
        widgets = {
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'time': 'Čas',
            'description': 'Popis',
            'order': 'Pořadí',
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['event', 'image', 'album_link', 'caption']
        widgets = {
            'event': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'album_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'caption': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'event': 'Akce',
            'image': 'Obrázek',
            'album_link': 'Odkaz na album',
            'caption': 'Popisek',
        }


class MapLocationForm(forms.ModelForm):
    class Meta:
        model = MapLocation
        fields = ['name', 'description', 'location_type', 'latitude', 'longitude', 'is_backlog']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'location_type': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'is_backlog': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'name': 'Název',
            'description': 'Popis',
            'location_type': 'Typ místa',
            'latitude': 'Zeměpisná šířka',
            'longitude': 'Zeměpisná délka',
            'is_backlog': 'V backlogu',
        }


class CalendarEntryForm(forms.ModelForm):
    class Meta:
        model = CalendarEntry
        fields = ['entry_type', 'start_date', 'end_date', 'note']
        widgets = {
            'entry_type': forms.Select(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'entry_type': 'Typ',
            'start_date': 'Od',
            'end_date': 'Do',
            'note': 'Poznámka',
        }


class RecurringEventForm(forms.ModelForm):
    class Meta:
        model = RecurringEvent
        fields = ['name', 'description', 'month', 'day', 'location']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'month': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12}),
            'day': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 31}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Název',
            'description': 'Popis',
            'month': 'Měsíc',
            'day': 'Den',
            'location': 'Místo',
        }


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message', 'event']
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Napište zprávu...'}),
            'event': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'message': 'Zpráva',
            'event': 'Akce (volitelné)',
        }


class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['tip_type', 'title', 'description', 'location', 'link']
        widgets = {
            'tip_type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
        }
        labels = {
            'tip_type': 'Typ tipu',
            'title': 'Název',
            'description': 'Popis',
            'location': 'Místo',
            'link': 'Odkaz',
        }


class DebtForm(forms.ModelForm):
    class Meta:
        model = Debt
        fields = ['recipient', 'amount', 'description', 'event']
        widgets = {
            'recipient': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'event': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'recipient': 'Komu dlužím',
            'amount': 'Částka (Kč)',
            'description': 'Popis',
            'event': 'Akce (volitelné)',
        }


class UndercoverWordPairForm(forms.ModelForm):
    class Meta:
        model = UndercoverWordPair
        fields = ['word1', 'word2', 'language']
        widgets = {
            'word1': forms.TextInput(attrs={'class': 'form-control'}),
            'word2': forms.TextInput(attrs={'class': 'form-control'}),
            'language': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'word1': 'Slovo 1',
            'word2': 'Slovo 2',
            'language': 'Jazyk',
        }

