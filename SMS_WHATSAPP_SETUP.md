# SMS and WhatsApp Notification Setup

This guide explains how to configure SMS and WhatsApp notifications for the OnlyFriends application using Twilio.

## Prerequisites

1. A Twilio account (sign up at https://www.twilio.com/)
2. Twilio Account SID and Auth Token (found in your Twilio Console)
3. A Twilio phone number (for SMS) or WhatsApp Business API access (for WhatsApp)

## Installation

The Twilio library is already included in `requirements.txt`. Install it with:

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Get Twilio Credentials

1. Log in to your [Twilio Console](https://www.twilio.com/console)
2. Find your **Account SID** and **Auth Token** on the dashboard
3. Get a phone number from Twilio (for SMS) or set up WhatsApp Business API

### 2. Configure Environment Variables

Set the following environment variables:

```bash
# Twilio Credentials
export TWILIO_ACCOUNT_SID="your_account_sid_here"
export TWILIO_AUTH_TOKEN="your_auth_token_here"
export TWILIO_PHONE_NUMBER="+1234567890"  # Your Twilio phone number

# WhatsApp (use Twilio sandbox for testing)
export TWILIO_WHATSAPP_NUMBER="whatsapp:+14155238886"  # Twilio sandbox number

# Enable notifications
export ENABLE_SMS_NOTIFICATIONS="true"
export ENABLE_WHATSAPP_NOTIFICATIONS="true"
```

### 3. WhatsApp Setup (Twilio Sandbox - For Testing)

For testing, you can use Twilio's WhatsApp sandbox:

1. Go to [Twilio Console > Messaging > Try it out > Send a WhatsApp message](https://www.twilio.com/console/sms/whatsapp/learn)
2. Follow the instructions to join the sandbox (send "join [code]" to the sandbox number)
3. Use the sandbox number: `whatsapp:+14155238886`

### 4. WhatsApp Setup (Production)

For production, you need:
1. A WhatsApp Business Account
2. Twilio WhatsApp Business API access
3. Your approved WhatsApp Business phone number

## User Configuration

Users need to:
1. Have a phone number in their profile (`UserProfile.phone_number`)
2. Have `notify_events=True` in their profile (default: True)
3. For WhatsApp: Have `notify_whatsapp=True` in their profile (default: False)

## Phone Number Format

Phone numbers should be in E.164 format (e.g., `+420123456789` for Czech Republic).

The system will automatically try to format phone numbers:
- If a number doesn't start with `+`, it assumes Czech Republic (+420)
- Removes leading zeros

## Testing

1. Set environment variables
2. Create a test event
3. Check logs for SMS/WhatsApp sending status
4. Verify notifications are received

## Costs

- **SMS**: Twilio charges per SMS sent (varies by country)
- **WhatsApp**: Twilio charges per WhatsApp message (varies by country)
- Check [Twilio Pricing](https://www.twilio.com/pricing) for current rates

## Troubleshooting

### SMS/WhatsApp not sending

1. Check that `ENABLE_SMS_NOTIFICATIONS` or `ENABLE_WHATSAPP_NOTIFICATIONS` is set to `"true"`
2. Verify Twilio credentials are correct
3. Check phone number format (must be E.164)
4. Check Twilio console for error messages
5. Review application logs for detailed error messages

### WhatsApp Sandbox Issues

- Make sure you've joined the Twilio WhatsApp sandbox
- Verify you're using the correct sandbox number
- Check that the recipient has also joined the sandbox (for testing)

## Disabling Notifications

To disable SMS or WhatsApp notifications, set the environment variables to `"false"`:

```bash
export ENABLE_SMS_NOTIFICATIONS="false"
export ENABLE_WHATSAPP_NOTIFICATIONS="false"
```

Or simply don't set the Twilio credentials - the system will skip SMS/WhatsApp sending if credentials are missing.


