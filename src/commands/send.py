from argparse import ArgumentParser, Namespace
from zope.interface import implementer
from src.commands import ICommand


@implementer(ICommand)
class SendCommand:
    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('--receiver', '-r',
                            required=True,
                            help="Receiver's email address, eg. 'avithewinner1508@gmail.com'")
        parser.add_argument('--subject', '-sub',
                            required=True,
                            help="Email's subject, eg. 'CA Endsem Submission [106118017]'")
        parser.add_argument('--body', '-b',
                            required=True,
                            help="Email's body file path, eg. '~/Desktop/body.txt' ")
        parser.add_argument('--attachment', '-a',
                            help="Email's attachment path, eg. '~/Desktop/106118017_CA_Endsem.pdf' ")

    def run_command(self, args: Namespace):
        print(args.receiver, args.subject, args.body, args.attachment)
