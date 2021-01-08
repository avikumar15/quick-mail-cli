from __future__ import print_function

import pickle
import os.path
import shutil

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from argparse import ArgumentParser, Namespace
from zope.interface import implementer
from src.quickmail.commands import ICommand
from src.quickmail.utils.misc import heavy_tick, heavy_exclamation, quick_mail_dir, quick_mail_creds_file, quick_mail_token_file

SCOPES = ['https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.readonly']


@implementer(ICommand)
class InitCommand:
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('filepath',
                            help="Path to credentials.json")

        parser.description = 'Use the init command to initialise the token and to set up your gmail account for ' \
                             'hassle-free mail deliveries'

    def check_creds_json(self, path):

        if os.path.exists(quick_mail_dir):
            if os.path.exists(quick_mail_creds_file):
                print('Credentials file already exists, skipping... ' + heavy_tick)
                return
            else:
                print('Placed credentials file ' + heavy_tick)
                shutil.copy2(path, quick_mail_creds_file)
        else:
            os.makedirs(quick_mail_dir)
            shutil.copy2(path, quick_mail_creds_file)
            print('Saved credentials file ' + heavy_tick)

    def run_command(self, args: Namespace):

        self.check_creds_json(args.filepath)
        creds = None

        try:
            if os.path.exists(quick_mail_token_file):
                with open(quick_mail_token_file, 'rb') as token:
                    creds = pickle.load(token)

            if not creds:
                flow = InstalledAppFlow.from_client_secrets_file(
                    quick_mail_creds_file, SCOPES)
                creds = flow.run_local_server(port=0)

                with open(quick_mail_token_file, 'wb') as token:
                    pickle.dump(creds, token)
                print('Generated token ' + heavy_tick)

            elif not creds.valid or creds.expired:
                creds.refresh(Request())
                with open(quick_mail_token_file, 'wb') as token:
                    pickle.dump(creds, token)
                print('Initialised token ' + heavy_tick)

            else:
                print('Initialised token ' + heavy_tick)

        except pickle.UnpicklingError:

            if os.path.exists(quick_mail_token_file):
                os.remove(quick_mail_token_file)

            print('Token file corrupted ' + heavy_exclamation + ' regenerating...')
            flow = InstalledAppFlow.from_client_secrets_file(
                quick_mail_creds_file, SCOPES)
            creds = flow.run_local_server(port=0)

            with open(quick_mail_token_file, 'wb') as token:
                pickle.dump(creds, token)

            print('Initialised token ' + heavy_tick)

    def get_desc(self) -> str:
        return 'initialise token and set your email id'
