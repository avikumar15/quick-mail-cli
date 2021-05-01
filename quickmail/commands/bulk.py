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
from time import sleep

from googleapiclient.discovery import build

from argparse import ArgumentParser, Namespace
from zope.interface import implementer
from quickmail.commands import ICommand
from quickmail.utils.misc import quick_mail_dir, quick_mail_token_file, grinning_face, heavy_tick, smiling_face, \
    party_popper_tada, heavy_exclamation, quick_mail_template_dir
from datetime import datetime
import subprocess


@implementer(ICommand)
class BulkCommand:
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('-r',
                            '--receivers',
                            required=True,
                            help="path to receivers' file '-r ~/receivers.txt' ")
        parser.add_argument('-sub',
                            '--subject',
                            required=True,
                            help="email's subject, eg. '-sub \"XYZ event\"'")
        parser.add_argument('-b',
                            '--body',
                            required=True,
                            help="path to email's body, eg. '-b ~/body.txt' ")
        parser.add_argument('-a',
                            '--attachment',
                            help="email's attachment path, eg. '-a ~/File.pdf' ")
        parser.add_argument('-l',
                            '--lessgo',
                            action='store_true',
                            help='skip confirmation before sending mail')

        parser.description = 'Use the bulk command to send mails in bulk. Add body file and receivers\' as an ' \
                             'argument and use optional --lessgo command for sending mails without confirmation '

    def run_command(self, args: Namespace):

        creds = None

        # if token.pickle file is missing, init command should be run
        if os.path.exists(quick_mail_token_file):
            with open(quick_mail_token_file, 'rb') as token:
                creds = pickle.load(token)
        else:
            print('Could not find credentials, please run init command first ' + heavy_exclamation + heavy_exclamation)
            exit(0)

        receiver_email = args.receivers
        subject = args.subject
        body = args.body
        attachment = args.attachment

        body_path = str(body)
        receiver_path = str(receiver_email)

        if not os.path.exists(body_path):
            print('Body file doesn\'t exists, exiting...')
            exit(0)

        f = open(body_path, "r")
        body_txt = f.read()
        f.close()

        print('\nAdded body of the mail ' + heavy_tick)

        if not os.path.exists(receiver_path):
            print('Receiver file doesn\'t exists, exiting...')
            exit(0)

        f = open(receiver_path, "r")
        receiver_txt = f.read()
        f.close()

        print('\nAdded receivers ' + heavy_tick)

        receivers = receiver_txt.split(',')

        print('Preparing to send mail ' + grinning_face)

        # build service
        service = build('gmail', 'v1', credentials=creds)

        # get user's email address from token file
        senders_email = service.users().getProfile(userId='me').execute()['emailAddress']

        # Show user mail summary
        print('\nFrom: ' + senders_email + '\nTo: Many' + '\nSubject: ' + subject + '\nBody\n' + body_txt +
              '\nAttachment Path: ' + (str(attachment) if attachment else 'No attachments') + '\n')

        if not args.lessgo:
            is_confirm = str(input('Confirm send? (Y/N): '))
            if is_confirm.lower() != 'y':
                print('Confirmation denied, exiting... ' + smiling_face + smiling_face + smiling_face)
                exit(0)

        if not attachment:
            message = MIMEText(body_txt)

            message['from'] = senders_email
            message['subject'] = subject

        else:
            message = MIMEMultipart()

            message['from'] = senders_email
            message['subject'] = subject

            message.attach(MIMEText(body_txt))
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

        num = len(receivers)

        print('Preparing to send mails to ' + str(num) + ' people')

        print()

        i = 0

        while i < (len(receivers)):
            a = min(45, len(receivers)-i)
            for j in range(a):
                message['to'] = str(receivers[i + j])

                raw = base64.urlsafe_b64encode(message.as_bytes())
                raw = raw.decode()
                final_message = {'raw': raw}

                try:
                    message_temp = (service.users().messages().send(userId=senders_email, body=final_message)
                                    .execute())
                except BaseException as e:
                    print('Could not send mail: ', e)
                    print('Mail id #' + str(i + j + 1))

            print('Mail delivered to set ' + str(int(i / 45) + 1) + heavy_tick + heavy_tick)
            i += 45

            sleep(1.5)

        print()
        print(party_popper_tada + party_popper_tada)
        print()

    def get_desc(self) -> str:
        return 'send mails in bulk'
