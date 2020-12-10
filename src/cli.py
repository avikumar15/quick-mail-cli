import argparse

from src.commands import BaseCommand

cli_description = 'A cli to quickly send a mail.'

parser = argparse.ArgumentParser(description=cli_description)

command = BaseCommand.instantiate(parser)
args = parser.parse_args()
command.run(args)
