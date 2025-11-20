from twilio.rest import Client
import os

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', '')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER', '')
TWILIO_WHATSAPP_NUMBER = os.environ.get('TWILIO_WHATSAPP_NUMBER','')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

message = client.messages.create(
  from_= TWILIO_WHATSAPP_NUMBER,  #'whatsapp:+14XXXXXXXX',
  content_sid=TWILIO_ACCOUNT_SID,
  content_variables='{"1":"12/1","2":"3pm"}',
  to= TWILIO_PHONE_NUMBER # 'whatsapp:+420111222333'
)

print("Message sent:", message.sid)
