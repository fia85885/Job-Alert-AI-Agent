from twilio.rest import Client
from config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, YOUR_WHATSAPP_NUMBER

def send_whatsapp_message(body):
    """Sends a message to your WhatsApp number via Twilio."""
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, YOUR_WHATSAPP_NUMBER]):
        print("Error: Twilio credentials are not fully configured.")
        return

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=body,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=YOUR_WHATSAPP_NUMBER
        )
        print(f"Message sent successfully! SID: {message.sid}")
    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")