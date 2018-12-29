from cliff.command import Command
from resteasycli.lib.initializer import initialize


class Init(Command):
    'Initialize template files in current directory'

    def take_action(self, args):
        initialize()