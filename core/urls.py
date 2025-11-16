from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Main menu tabs
    path('', views.index, name='index'),
    path('events/', views.events_list, name='events_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('photos/', views.photos_list, name='photos_list'),
    path('maps/', views.maps_list, name='maps_list'),
    path('weather/', views.weather_alerts, name='weather_alerts'),
    path('calendar/', views.calendar_view, name='calendar_view'),
    path('recurring-events/', views.recurring_events, name='recurring_events'),
    path('birthdays/', views.birthdays, name='birthdays'),
    path('chat/', views.chat, name='chat'),
    path('tips/', views.tips_list, name='tips_list'),
    path('debts/', views.debts_list, name='debts_list'),
    path('undercover/', views.undercover, name='undercover'),
    path('notifications/', views.notifications, name='notifications'),
]

