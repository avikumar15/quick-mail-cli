import inspect
from contextlib import suppress
from argparse import ArgumentParser, Namespace
from typing import Dict

from zope.interface import Interface, implementer
from zope.interface.exceptions import Invalid, MultipleInvalid

from quickmail.utils.misc import walk_modules, command_dir_path


class ICommand(Interface):

    def add_arguments(parser: ArgumentParser) -> None:
        pass

    def run_command(args: Namespace) -> None:
        pass

    def get_desc(self) -> str:
        pass


def populate_commands(cls):

    # finding all files inside src.commands, and returning files which have classes inherited from ICommand
    for module in walk_modules(command_dir_path):
        for obj in vars(module).values():
            with suppress(Invalid, MultipleInvalid):
                if (
                        inspect.isclass(obj)
                        # and verifyClass(ICommand, obj)
                        and obj.__module__ == module.__name__
                        and not obj == cls
                ):
                    yield obj


@implementer(ICommand)
class BaseCommand:

    def __init__(self, parser: ArgumentParser):
        # commands_dict contains a dictionary from the command name to the class that implements it
        self.commands_dict: Dict[str, BaseCommand] = {}

        # populating the dict
        for cmd in populate_commands(BaseCommand):
            command_name = cmd.__module__.split('.')[-1]
            self.commands_dict[command_name] = cmd()

        # add options to parser
        self.add_arguments(parser)

    def add_arguments(self, parser: ArgumentParser) -> None:

        sub_parser = parser.add_subparsers(dest='command')
        # add all the commands
        for name, subcommand in self.commands_dict.items():
            subcommand_parser = sub_parser.add_parser(name, help=subcommand.get_desc())
            # call add_options of the specific command class
            subcommand.add_arguments(subcommand_parser)

    def run_command(self, args: Namespace):
        # if command is valid, run the run_command function of the specific class
        if args.command:
            self.commands_dict[args.command].run_command(args)
