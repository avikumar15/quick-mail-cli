from __future__ import print_function

import os
from argparse import ArgumentParser, Namespace
from zope.interface import implementer
from src.quickmailcli.commands import ICommand
from src.quickmailcli.utils.misc import quick_mail_dir, heavy_tick


@implementer(ICommand)
class ClearCommand:
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('--justdoit', '-j',
                            action='store_true',
                            help='Clear storage completely')

    def run_command(self, args: Namespace):
        if not os.path.exists(quick_mail_dir):
            print('Storage already is empty ' + heavy_tick)
            return

        if args.fuckit:
            for file in os.listdir(quick_mail_dir):
                os.remove(quick_mail_dir + '/' + file)
        else:
            saved_files = [file for file in os.listdir(quick_mail_dir) if file.endswith('.txt')]
            for file in saved_files:
                os.remove(quick_mail_dir + '/' + file)

        print('Storage cleared ' + heavy_tick + heavy_tick)
