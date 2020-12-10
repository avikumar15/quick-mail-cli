import os
import inspect
from contextlib import suppress
from argparse import ArgumentParser, ArgumentError, Namespace
from typing import Dict

from zope.interface import Interface, implementer
from zope.interface.exceptions import Invalid, MultipleInvalid
from zope.interface.verify import verifyClass

from src.utils.misc import walk_modules


class ICommand(Interface):

    def add_commands(parser: ArgumentParser) -> None:
        pass

    def run(args: Namespace) -> None:
        pass


def iter_subcommands(cls):
    for module in walk_modules('src.commands'):
        for obj in vars(module).values():
            with suppress(Invalid, MultipleInvalid):
                if (
                        inspect.isclass(obj)
                        and verifyClass(ICommand, obj)
                        and obj.__module__ == module.__name__
                        and not obj == cls
                ):
                    print(obj)
                    yield obj


@implementer(ICommand)
class BaseCommand:

    def __init__(self):
        self.subcommands: Dict[str, BaseCommand] = {}
        for cmd in iter_subcommands(BaseCommand):
            cmdname = cmd.__module__.split('.')[-1]
            self.subcommands[cmdname] = cmd()

    @classmethod
    def instantiate(cls, parser: ArgumentParser):
        obj = cls()
        obj.add_options(parser)
        return obj

    def add_options(self, parser: ArgumentParser) -> None:
        sub_parsers = parser.add_subparsers(dest='command')
        for name, subcmd in self.subcommands.items():
            subcmd_parser = sub_parsers.add_parser(name)
            subcmd.add_options(subcmd_parser)

    def run(self, args: Namespace):
        if args.command:
            self.subcommands[args.command].run(args)
