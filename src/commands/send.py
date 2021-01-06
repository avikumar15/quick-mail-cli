from __future__ import print_function

import mimetypes
import os
import pickle
import base64
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build

from argparse import ArgumentParser, Namespace
from zope.interface import implementer
from src.commands import ICommand


@implementer(ICommand)
class SendCommand:
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('--receiver', '-r',
                            required=True,
                            help="Receiver's email address, eg. 'avithewinner1508@gmail.com'")
        parser.add_argument('--subject', '-sub',
                            required=True,
                            help="Email's subject, eg. 'CA Endsem Submission [106118017]'")
        parser.add_argument('--body', '-b',
                            required=True,
                            help="Email's body file path, eg. '~/Desktop/body.txt' ")
        parser.add_argument('--attachment', '-a',
                            help="Email's attachment path, eg. '~/Desktop/106118017_CA_Endsem.pdf' ")

    def run_command(self, args: Namespace):

        receiver_email = args.receiver
        subject = args.subject
        body = args.body
        attachment = args.attachment

        print(receiver_email, subject, body, attachment)

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        else:
            print('Run init command before send')
            exit(0)

        service = build('gmail', 'v1', credentials=creds)
        service.users().messages()
        senders_email = service.users().getProfile(userId='me').execute()['emailAddress']

        is_confirm = str(input('Confirm send? (Y/N): '))

        if is_confirm.lower() != 'y':
            print('Confirmation denied, exiting...')
            exit(0)

        if not attachment:
            message = MIMEText(body)

            message['to'] = receiver_email
            message['from'] = senders_email
            message['subject'] = subject

        else:
            message = MIMEMultipart()
            message['to'] = receiver_email
            message['from'] = senders_email
            message['subject'] = subject

            message.attach(MIMEText(body))

            content_type, encoding = mimetypes.guess_type(attachment)
            if content_type is None or encoding is not None:
                content_type = 'application/octet-stream'
            main_type, sub_type = content_type.split('/', 1)

            if main_type == 'text':
                fp = open(attachment, 'rb')
                msg = MIMEText(str(fp.read()), _subtype=sub_type)
                fp.close()
            elif main_type == 'image':
                fp = open(attachment, 'rb')
                msg = MIMEImage(fp.read(), _subtype=sub_type)
                fp.close()
            elif main_type == 'audio':
                fp = open(attachment, 'rb')
                msg = MIMEAudio(fp.read(), _subtype=sub_type)
                fp.close()
            else:
                fp = open(attachment, 'rb')
                msg = MIMEApplication(fp.read(), _subtype=sub_type)
                fp.close()

            filename = os.path.basename(attachment)
            msg.add_header('Content-Disposition', 'attachment', filename=filename)
            message.attach(msg)

        raw = base64.urlsafe_b64encode(message.as_bytes())
        raw = raw.decode()
        message = {'raw': raw}

        try:
            message = (service.users().messages().send(userId=senders_email, body=message)
                       .execute())
            print(message)
        except BaseException as e:
            print('Could not send message: ', e)

