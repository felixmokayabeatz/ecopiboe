from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
from google.auth.transport.requests import Request
from ..models import UserEmailAccount

def send_user_email(user, subject, message, recipient):
    user_email_account = UserEmailAccount.objects.get(user=user)
    credentials = Credentials(
        token=user_email_account.access_token,
        refresh_token=user_email_account.refresh_token,
        token_uri='https://oauth2.googleapis.com/token',
        client_id='your-client-id',
        client_secret='your-client-secret'
    )

    if credentials.expired:
        credentials.refresh(Request())

    service = build('gmail', 'v1', credentials=credentials)
    message = MIMEText(message)
    message['to'] = recipient
    message['from'] = user.email
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    message = {
        'raw': raw_message
    }

    service.users().messages().send(userId='me', body=message).execute()
