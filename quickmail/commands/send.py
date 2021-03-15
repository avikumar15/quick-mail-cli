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
from quickmail.commands import ICommand
from quickmail.utils.misc import quick_mail_dir, quick_mail_token_file, grinning_face, heavy_tick, smiling_face, \
    party_popper_tada, heavy_exclamation, quick_mail_template_dir
from datetime import datetime
import subprocess


@implementer(ICommand)
class SendCommand:
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('-r',
                            '--receiver',
                            required=True,
                            help="receiver's email address, eg. '-r \"xyz@gmail.com\"' ")
        parser.add_argument('-sub',
                            '--subject',
                            required=True,
                            help="email's subject, eg. '-sub \"XYZ submission\"'")
        parser.add_argument('-t',
                            '--template',
                            help="template of email body, eg. '-t=\"assignment_template\"' ")
        parser.add_argument('-b',
                            '--body',
                            help="email's body, eg. '-b \"Message Body Comes Here\"'")
        parser.add_argument('-a',
                            '--attachment',
                            help="email's attachment path, eg. '~/Desktop/XYZ_Endsem.pdf' ")
        parser.add_argument('-l',
                            '--lessgo',
                            action='store_true',
                            help='skip confirmation before sending mail')

        parser.description = 'Use the send command to send mail. Body can be passed as an argument, or typed in a ' \
                             'nano shell. Use optional --lessgo command for sending mail without confirmation'

    def run_command(self, args: Namespace):

        creds = None

        # if token.pickle file is missing, init command should be run
        if os.path.exists(quick_mail_token_file):
            with open(quick_mail_token_file, 'rb') as token:
                creds = pickle.load(token)
        else:
            print('Could not find credentials, please run init command first ' + heavy_exclamation + heavy_exclamation)
            exit(0)

        receiver_email = args.receiver
        subject = args.subject
        body = args.body
        attachment = args.attachment
        template = args.template

        if not body and not template:
            body_file_name = '/' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '.txt'
            file_path = quick_mail_dir + body_file_name

            f = open(file_path, "x")
            # print(file_path)
            subprocess.call(['nano', file_path])
            f.close()
            f = open(file_path, "r")
            body = f.read()
            # print(body)
            print('\nAdded body of the mail ' + heavy_tick)
            f.close()

        elif not body:

            template_path = quick_mail_template_dir + template + '.txt'

            if not os.path.exists(template_path):
                print('Template doesn\'t exists, exiting...')
                exit(0)

            f = open(template_path, "r")
            template_txt = f.read()
            f.close()

            body_file_name = '/' + datetime.now().strftime("%d_%m_%Y_%H_%M_%S") + '.txt'
            file_path = quick_mail_dir + body_file_name

            f = open(file_path, "a")
            f.write(template_txt)
            f.close()

            subprocess.call(['nano', file_path])
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
        print('\nFrom: ' + senders_email + '\nTo: ' + receiver_email + '\nSubject: ' + subject + '\nBody\n' + body +
              '\nAttachment Path: ' + (str(attachment) if attachment else 'No attachments') + '\n')

        if not args.lessgo:
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

    def get_desc(self) -> str:
        return 'send the mail'
