from __future__ import print_function

import pickle
import os.path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from argparse import ArgumentParser, Namespace
from zope.interface import implementer
from src.commands import ICommand

SCOPES = ['https://www.googleapis.com/auth/gmail.send',
          'https://www.googleapis.com/auth/gmail.readonly']


@implementer(ICommand)
class InitCommand:
    def add_arguments(self, parser: ArgumentParser) -> None:
        pass

    def run_command(self, args: Namespace):
        creds = None
        try:
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)

            if not creds:
                print('Have to generate token.pickle file')
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
                print('Generated token.pickle file')

            if not creds.valid or creds.expired:
                print('Have to refresh token.pickle file')
                creds.refresh(Request())
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
                print('Reinitialised token file')

            else:
                print('Token file already exists, skipping...')

        except pickle.UnpicklingError:

            if os.path.exists('token.pickle'):
                os.remove('token.pickle')

            print('token.pickle file is corrupted.')
            print('Have to generate token file')
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

            print('Generated token file')
