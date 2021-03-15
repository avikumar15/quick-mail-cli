from __future__ import print_function

import os
import subprocess
from argparse import ArgumentParser, Namespace
from zope.interface import implementer
from quickmail.commands import ICommand
from quickmail.utils.misc import heavy_tick, quick_mail_template_dir, party_popper_tada


@implementer(ICommand)
class ClearCommand:

    def add_arguments(self, parser: ArgumentParser) -> None:

        subp = parser.add_subparsers(dest='template_subcommand')

        subp.add_parser('add', help='add a new template') \
            .add_argument('-n',
                          '--templatename',
                          required=True,
                          help='name of the new template')

        subp.add_parser('listall', help='list all templates')

        subp.add_parser('edit', help='edit a particular template') \
            .add_argument('-n',
                          '--templatename',
                          required=True,
                          help='name of the new template')

        parser.description = 'manage mail templates'

    def run_command(self, args: Namespace):

        if args.template_subcommand == 'add':
            if not os.path.exists(quick_mail_template_dir):
                os.makedirs(quick_mail_template_dir)

            file_path = quick_mail_template_dir + args.templatename + '.txt'

            f = open(file_path, "x")
            # print(file_path)
            subprocess.call(['nano', file_path])
            f.close()

            print('Template created, at ' + file_path + ' ' + party_popper_tada + party_popper_tada)

        elif args.template_subcommand == 'listall':
            templates = [file for file in os.listdir(quick_mail_template_dir) if file.endswith('.txt')]
            for template in reversed(templates):
                # remove '.txt' from template name
                template = template[:-4]
                print(template)
        elif args.template_subcommand == 'edit':

            file_path = quick_mail_template_dir + args.templatename + '.txt'

            if not os.path.exists(file_path):
                print('Template doesn\'t exists, created new one at ' + file_path + ' ' + heavy_tick)
                f = open(file_path, "x")
                f.close()

            f = open(file_path, "a")

            subprocess.call(['nano', file_path])
            f.close()

            print('Template edited, check: ' + file_path + ' ' + party_popper_tada + party_popper_tada)

    def get_desc(self) -> str:
        return 'manage templates of mail body'
