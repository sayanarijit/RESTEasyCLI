import sys
from cliff.app import App
from cliff.help import HelpCommand
from cliff.commandmanager import CommandManager

from resteasycli.config import Config
from resteasycli.lib.workspace import Workspace
from resteasycli.exceptions import FileNotFoundException


class CLIApp(App):
    '''The main CLI app'''
    def __init__(self):
        super(CLIApp, self).__init__(
            description=Config.DESCRIPTION,
            version=Config.VERSION,
            command_manager=CommandManager('cliff.recli.pre_init'),
            deferred_help=True,
        )
        # TODO: Add auto completion the best way
        # self.command_manager.add_command(
        #     'complete', CompleteCommand)
        self.workspace = None

    def initialize_app(self, argv):
        self.LOG.debug('initializing app')
        try:
            self.workspace = Workspace(logger=self.LOG)
            self.command_manager.namespace = 'cliff.recli.post_init'
            self.command_manager.load_commands(self.command_manager.namespace)
        except FileNotFoundException:
            pass

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('preparing to run command {}'.format(
            cmd.__class__.__name__))

    def clean_up(self, cmd, result, err):
        self.LOG.debug('cleaning up {}'.format(cmd.__class__.__name__))
        if err:
            self.LOG.debug('got an error: {}'.format(err))


def main(argv=sys.argv[1:]):
    app = CLIApp()
    try:
        return app.run(argv)
    except Exception as e:
        sys.stderr.write('error: {}\n'.format(e))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
