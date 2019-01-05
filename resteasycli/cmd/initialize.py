import logging
from cliff.command import Command

from resteasycli.config import Config
from resteasycli.lib.workspace import WorkspaceTemplates


class Init(Command):
    'Initialize template files in current directory'

    def get_parser(self, prog_name):
        parser = super(Init, self).get_parser(prog_name)
        parser.add_argument('-f', '--force', action='store_true')
        parser.add_argument('-e', '--extension', help=('|'.join(Config.SUPPORTED_FILE_EXTENSIONS)),
                default=Config.DEFAULT_FILE_EXTENSION)
        return parser

    def take_action(self, args):
        WorkspaceTemplates.initialize(force=args.force, extension=args.extension)
