from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.db import models
from .models import Event, UserProfile, Notification
from .sms import send_sms, send_whatsapp, format_phone_number
import logging

logger = logging.getLogger(__name__)

VALID_SCOPES = {'notify_all', 'notify_invited', 'notify_none'}


def send_event_notification(event, scope='notify_all', notification_reason='created'):
    """
    Send notifications (email, SMS, WhatsApp) when an event is created or updated.
    scope:
        - notify_all: everyone with contact info
        - notify_invited: exclude users listed in excluded_users
        - notify_none: skip notifications entirely
    notification_reason:
        - created: default, used for new events
        - updated: used for edits
    """
    scope = scope or 'notify_all'
    if scope not in VALID_SCOPES:
        scope = 'notify_all'
    
    if scope == 'notify_none':
        logger.info('Notification scope set to none; skipping notifications.')
        return
    
    notification_reason = notification_reason if notification_reason in {'created', 'updated'} else 'created'
    
    # Prepare copy based on reason
    if notification_reason == 'updated':
        subject = f'Událost upravena: {event.title}'
        intro_line = 'Událost, které se chcete účastnit, byla upravena.'
        notification_text = f'Událost {event.title} byla upravena.'
    else:
        subject = f'Nová událost: {event.title}'
        intro_line = 'Byla vytvořena nová událost, která by vás mohla zajímat.'
        notification_text = f'Byla vytvořena událost {event.title}.'
    
    # Base queryset
    if scope == 'notify_invited':
        excluded_user_ids = list(event.excluded_users.values_list('id', flat=True))
        users_to_notify = User.objects.exclude(id__in=excluded_user_ids)
    else:
        users_to_notify = User.objects.all()
    
    # Everyone must have at least email or phone
    users_to_notify = users_to_notify.filter(
        models.Q(email__isnull=False) | models.Q(profile__phone_number__isnull=False)
    ).distinct()
    
    # Exclude organizer if exists
    if event.organizer:
        users_to_notify = users_to_notify.exclude(id=event.organizer.id)
    
    # Filter by notify_events preference
    eligible_users = []
    for user in users_to_notify:
        try:
            profile = user.profile
            if profile.notify_events:
                eligible_users.append(user)
        except (UserProfile.DoesNotExist, AttributeError):
            eligible_users.append(user)
    
    if not eligible_users:
        logger.info('No eligible users for notifications.')
        return
    
    # Gather event details
    event_date = event.start_date.strftime('%d.%m.%Y %H:%M') if event.start_date else 'Datum není určeno'
    event_location = event.location or (event.map_location.name if event.map_location else '') or 'Místo není určeno'
    organizer_name = event.organizer.get_full_name() or event.organizer.username if event.organizer else 'Neznámý'
    
    site_url = getattr(settings, 'SITE_URL', 'http://127.0.0.1:8000')
    event_url = f"{site_url}{reverse('core:event_detail', args=[event.id])}"
    
    description_text = f'\nPopis: {event.description}\n' if event.description else ''
    full_message = f"""Dobrý den,

{intro_line}

Událost: {event.title}
Organizátor: {organizer_name}
Datum: {event_date}
Místo: {event_location}
Typ: {'Veřejná' if event.event_type == 'public' else 'Tajná'}{description_text}
Detail události: {event_url}

S pozdravem,
Tým OnlyFriends"""
    
    short_message = f"Událost: {event.title}\n{event_date}\n{event_location}\n{event_url}"
    if len(short_message) > 300:
        short_message = f"Událost: {event.title}\n{event_date}\n{event_url}"
    
    for user in eligible_users:
        try:
            try:
                profile = user.profile
            except (UserProfile.DoesNotExist, AttributeError):
                profile = None
            
            # Email
            if user.email:
                try:
                    send_mail(
                        subject=subject,
                        message=full_message,
                        from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@onlyfriends.com'),
                        recipient_list=[user.email],
                        fail_silently=True,
                    )
                except Exception as email_error:
                    logger.error(f'Failed to send email to {user.email}: {email_error}')
            
            # SMS / WhatsApp
            whatsapp_sent = False
            if profile and profile.phone_number:
                phone_number = format_phone_number(profile.phone_number)
                if phone_number:
                    send_sms(phone_number, short_message)
                    if profile.notify_whatsapp:
                        whatsapp_sent = send_whatsapp(phone_number, short_message)
            else:
                whatsapp_sent = False
            
            # Save notification record
            try:
                Notification.objects.create(
                    user=user,
                    notification_type='event',
                    title=subject,
                    message=notification_text,
                    sent_whatsapp=whatsapp_sent,
                    sent_app=False,
                )
            except Exception as notification_error:
                logger.error(f'Failed to store notification for {user.username}: {notification_error}')
        
        except Exception as user_error:
            logger.error(f'Failed to process notifications for {user.username}: {user_error}')

