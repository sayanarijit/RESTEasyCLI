from cliff.command import Command
from resteasycli.lib.workspace import WorkspaceTemplates


class Init(Command):
    'Initialize template files in current directory'

    def get_parser(self, prog_name):
        parser = super(Init, self).get_parser(prog_name)
        parser.add_argument('-f', '--force', action='store_true')
        return parser

    def take_action(self, args):
        WorkspaceTemplates.initialize(force=args.force)
