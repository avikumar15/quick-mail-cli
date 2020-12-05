from __future__ import print_function

import base64
import pickle
import os.path
from email.mime.text import MIMEText

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.send']


def main():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    to_email = str(input('Enter to email address: '))
    subject = str(input('Enter subject of mail: '))
    body = str(input('Enter mail body: '))

    is_attachment = str(input('Do you want to attach files? (Y/n): '))

    if is_attachment.lower() == 'y':
        path = str(input('Enter attachment path: '))

    confirm_send = str(input('Confirm send? (Y/n): '))
    service.users().messages()

    message = MIMEText(body)

    if confirm_send.lower() == 'y':
        message['to'] = to_email
        message['subject'] = subject
        raw = base64.urlsafe_b64encode(message.as_bytes())
        raw = raw.decode()
        message = {'raw': raw}
    else:
        exit(0)

    try:
        message = (service.users().messages().send(userId=to_email, body=message)
                   .execute())
        print(message)
    except BaseException as e:
        print(e)


if __name__ == '__main__':
    main()
