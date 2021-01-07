from __future__ import print_function

import mimetypes
import os
import pickle
import base64
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from googleapiclient.discovery import build

from argparse import ArgumentParser, Namespace
from zope.interface import implementer
from src.commands import ICommand
from src.utils.misc import quick_mail_dir, quick_mail_token_file, wink_face, grinning_face, heavy_tick, smiling_face, \
    party_popper_tada
from datetime import datetime
import subprocess


@implementer(ICommand)
class SendCommand:
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('--receiver', '-r',
                            required=True,
                            help="Receiver's email address, eg. '-r \"avithewinner1508@gmail.com\"' ")
        parser.add_argument('--subject', '-sub',
                            required=True,
                            help="Email's subject, eg. '-sub \"CA Endsem Submission'\"")
        parser.add_argument('--body', '-b',
                            help="Email's body file path, eg. '-b ~/Desktop/body.txt' or '-b \"Message Body Comes "
                                 "Here\"' ")
        parser.add_argument('--attachment', '-a',
                            help="Email's attachment path, eg. '~/Desktop/CA_Endsem.pdf' ")

    def run_command(self, args: Namespace):

        creds = None

        # if token.pickle file is missing, init command should be run
        if os.path.exists(quick_mail_token_file):
            with open(quick_mail_token_file, 'rb') as token:
                creds = pickle.load(token)
        else:
            print('Run init command before send')
            exit(0)

        receiver_email = args.receiver
        subject = args.subject
        body = args.body
        attachment = args.attachment

        if not body:
            body_file_name = '/' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '.txt'
            file_path = quick_mail_dir+body_file_name

            f = open(file_path, "x")
            # print(file_path)
            subprocess.call(['nano', file_path])
            f.close()
            f = open(file_path, "r")
            body = f.read()
            # print(body)
            print('\nAdded body of the mail ' + heavy_tick)
            f.close()
        # Hacky fix to add a new line if body is not null
        else:
            print()

        print('Preparing to send mail ' + grinning_face)

        # build service
        service = build('gmail', 'v1', credentials=creds)

        # get user's email address from token file
        senders_email = service.users().getProfile(userId='me').execute()['emailAddress']

        # Show user mail summary
        print('\nFrom: ' + senders_email + '\nTo: '+receiver_email + '\nSubject: ' + subject + '\nBody\n' + body +
              '\nAttachment Path: ' + (str(attachment) if attachment else 'No attachments') + '\n')

        is_confirm = str(input('Confirm send? (Y/N): '))

        if is_confirm.lower() != 'y':
            print('Confirmation denied, exiting... ' + smiling_face + smiling_face + smiling_face)
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
                msg = MIMEText(str(fp.read().decode('utf-8')), _subtype=sub_type)
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
            print('Mail delivered ' + party_popper_tada + party_popper_tada + party_popper_tada)
        except BaseException as e:
            print('Could not send message: ', e)

        print()