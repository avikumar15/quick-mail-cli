from __future__ import print_function

import pickle
import os.path
import shutil

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from argparse import ArgumentParser, Namespace
from zope.interface import implementer
from src.commands import ICommand
from src.utils.misc import heavy_tick, heavy_exclamation

SCOPES = ['https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.readonly']


@implementer(ICommand)
class InitCommand:
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('filepath',
                            help="Path to credentials.json")

    def check_creds_json(self, path):

        quick_mail_dir = os.path.expanduser('~/.quickmail')
        quick_mail_creds_file = os.path.expanduser('~/.quickmail/credentials.json')

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

        token_path = os.path.expanduser('~/.quickmail/token.pickle')
        creds_path = os.path.expanduser('~/.quickmail/credentials.json')

        try:
            if os.path.exists(token_path):
                with open(token_path, 'rb') as token:
                    creds = pickle.load(token)

            if not creds:
                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_path, SCOPES)
                creds = flow.run_local_server(port=0)

                with open(token_path, 'wb') as token:
                    pickle.dump(creds, token)
                print('Generated token ' + heavy_tick)

            elif not creds.valid or creds.expired:
                creds.refresh(Request())
                with open(token_path, 'wb') as token:
                    pickle.dump(creds, token)
                print('Initialised token ' + heavy_tick)

            else:
                print('Initialised token ' + heavy_tick)

        except pickle.UnpicklingError:

            if os.path.exists(token_path):
                os.remove(token_path)

            print('Token file corrupted ' + heavy_exclamation + ' regenerating...')
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES)
            creds = flow.run_local_server(port=0)

            with open(token_path, 'wb') as token:
                pickle.dump(creds, token)

            print('Initialised token ' + heavy_tick)
