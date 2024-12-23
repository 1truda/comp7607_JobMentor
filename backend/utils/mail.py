import os.path
import base64

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If a new user try to run the code, please delete the token.json file
class GmailUtils:
    def __init__(self, token_file_path='token.json', credentials_file_path='credentials.json'):
        self.SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
        self.token_file = token_file_path
        self.credentials_file = credentials_file_path

    def get_credentials(self):
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES
                )
                creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
                with open("token.json", "w") as token:
                    token.write(creds.to_json())
        return creds

    def get_messages_list(self, q=""):
        try:
            res = []
            service = build('gmail', 'v1', credentials=self.get_credentials())
            results = service.users().messages().list(userId='me', q=q).execute()
            res += results.get('messages', [])
            while 'nextPageToken' in results:
                page_token = results['nextPageToken']
                results = service.users().messages().list(userId='me', q=q, pageToken=page_token).execute()
                res += results.get('messages', [])
            return res
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None

    def get_message_with_subject_and_time(self, message_id):
        try:
            service = build('gmail', 'v1', credentials=self.get_credentials())
            message = service.users().messages().get(userId='me', id=message_id).execute()
            content = ""
            if message['payload']['body']['size'] == 0:
                content = base64.b64decode(message['payload']['parts'][0]['body']['data']).decode('utf-8')
            else:
                content = base64.b64decode(message['payload']['body']['data']).decode('utf-8')
            date = message['internalDate']
            subject = ""
            for header in message['payload']['headers']:
                if header['name'] == 'Subject':
                    subject = header['value']
            return subject, content, date
        except HttpError as error:
            print(f'An error occurred: {error}')

    def get_message_raw(self, message_id):
        service = build('gmail', 'v1', credentials=self.get_credentials())
        message = service.users().messages().get(userId='me', id=message_id).execute()

        return message


if __name__ == '__main__':
    gmail_utils = GmailUtils()
    print(gmail_utils.get_messages_list(q="interview"))
