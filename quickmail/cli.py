import argparse

from quickmail.commands import BaseCommand


def execute():
    cli_description = 'A command line interface to send mail without any hassle'

    parser = argparse.ArgumentParser(description=cli_description)

    parser.add_argument('-v',
                        '--version',
                        action='version',
                        version='%(prog)s 1.0.3',
                        help='print current cli version')

    command = BaseCommand(parser)
    args = parser.parse_args()
    command.run_command(args)
