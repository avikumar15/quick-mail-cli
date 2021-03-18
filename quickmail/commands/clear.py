from __future__ import print_function

import os
from argparse import ArgumentParser, Namespace
from zope.interface import implementer
from quickmail.commands import ICommand
from quickmail.utils.misc import quick_mail_dir, heavy_tick, quick_mail_template_dir


@implementer(ICommand)
class ClearCommand:
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('-j',
                            '--justdoit',
                            action='store_true',
                            help='clear storage including the credentials and token')
        parser.description = 'Use the clear command to clear all email body that are saved in your home directories. ' \
                             'Additionally, pass --justdoit to remove the credential files as well'

    def run_command(self, args: Namespace):
        if not os.path.exists(quick_mail_dir):
            print('Storage already is empty ' + heavy_tick)
            return

        if args.justdoit:
            saved_files = [file for file in os.listdir(quick_mail_dir) if (file.endswith('.json') or file.endswith('.pickle'))]
            for file in saved_files:
                os.remove(quick_mail_dir + '/' + file)
        else:
            saved_files = [file for file in os.listdir(quick_mail_dir) if file.endswith('.txt')]
            for file in saved_files:
                os.remove(quick_mail_dir + '/' + file)

        saved_files = [file for file in os.listdir(quick_mail_template_dir) if file.endswith('.txt')]
        for file in saved_files:
            os.remove(quick_mail_template_dir + file)

        print('Storage cleared ' + heavy_tick + heavy_tick)

    def get_desc(self) -> str:
        return 'clear the body of message from local or even the token if --justdoit argument is added'
