from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Main menu tabs
    path('', views.index, name='index'),
    
    # Events
    path('events/', views.events_list, name='events_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:event_id>/delete/', views.event_delete, name='event_delete'),
    
    # Photos and Albums
    path('photos/', views.photos_list, name='photos_list'),
    path('photos/create/', views.photo_create, name='photo_create'),
    path('photos/create/album/<int:album_id>/', views.photo_create, name='photo_create_album'),
    path('photos/create/sub-album/<int:sub_album_id>/', views.photo_create, name='photo_create_sub_album'),
    path('photos/<int:photo_id>/edit/', views.photo_edit, name='photo_edit'),
    path('photos/<int:photo_id>/like/', views.photo_like, name='photo_like'),
    path('albums/create/', views.album_create, name='album_create'),
    path('albums/create/event/<int:event_id>/', views.album_create, name='album_create_event'),
    path('albums/<int:album_id>/', views.album_detail, name='album_detail'),
    path('albums/<int:album_id>/edit/', views.album_edit, name='album_edit'),
    path('albums/<int:album_id>/sub-album/create/', views.sub_album_create, name='sub_album_create'),
    path('sub-albums/<int:sub_album_id>/', views.sub_album_detail, name='sub_album_detail'),
    
    # Maps
    path('maps/', views.maps_list, name='maps_list'),
    path('maps/create/', views.map_create, name='map_create'),
    path('maps/<int:location_id>/edit/', views.map_edit, name='map_edit'),
    
    # Weather
    path('weather/', views.weather_alerts, name='weather_alerts'),
    
    # Calendar
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('calendar/create/', views.calendar_entry_create, name='calendar_entry_create'),
    path('calendar/<int:entry_id>/edit/', views.calendar_entry_edit, name='calendar_entry_edit'),
    
    # Recurring events
    path('recurring-events/', views.recurring_events, name='recurring_events'),
    path('recurring-events/create/', views.recurring_event_create, name='recurring_event_create'),
    path('recurring-events/<int:event_id>/edit/', views.recurring_event_edit, name='recurring_event_edit'),
    
    # Birthdays
    path('birthdays/', views.birthdays, name='birthdays'),
    
    # Chat
    path('chat/', views.chat, name='chat'),
    
    # Tips
    path('tips/', views.tips_list, name='tips_list'),
    path('tips/create/', views.tip_create, name='tip_create'),
    path('tips/<int:tip_id>/edit/', views.tip_edit, name='tip_edit'),
    
    # Debts
    path('debts/', views.debts_list, name='debts_list'),
    path('debts/create/', views.debt_create, name='debt_create'),
    path('debts/<int:debt_id>/settle/', views.debt_settle, name='debt_settle'),
    
    # Undercover
    path('undercover/', views.undercover, name='undercover'),
    path('undercover/create/', views.undercover_wordpair_create, name='undercover_wordpair_create'),
    
    # Notifications
    path('notifications/', views.notifications, name='notifications'),
]

