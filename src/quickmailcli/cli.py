import argparse

from src.quickmailcli.commands import BaseCommand

cli_description = 'A command line interface to send a quick mail'

parser = argparse.ArgumentParser(description=cli_description)

command = BaseCommand(parser)
args = parser.parse_args()
command.run_command(args)
