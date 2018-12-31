import sys
from cliff.app import App
from cliff.complete import CompleteCommand
from cliff.commandmanager import CommandManager
from resteasy import HTTPError, InvalidResponseError

from resteasycli import exceptions
from resteasycli.config import Config


class CLIApp(App):
    '''The main CLI app'''
    def __init__(self):
        super(CLIApp, self).__init__(
            description=Config.DESCRIPTION,
            version=Config.VERSION,
            command_manager=CommandManager('cliff.recli'),
            deferred_help=True,
        )
        # TODO: Add auto completion the best way
        # self.command_manager.add_command(
        #     'complete', CompleteCommand)

    def initialize_app(self, argv):
        self.LOG.debug('initializing app')

    def prepare_to_run_command(self, cmd):
        self.LOG.debug('preparing to run command %s', cmd.__class__.__name__)

    def clean_up(self, cmd, result, err):
        self.LOG.debug('cleaning up %s', cmd.__class__.__name__)
        if err:
            self.LOG.debug('got an error: %s', err)


def main(argv=sys.argv[1:]):
    app = CLIApp()
    try:
        return app.run(argv)
    except (HTTPError, InvalidResponseError,
            exceptions.MethodNotAllowedException,
            exceptions.FileNotFoundException,
            exceptions.FileExtensionNotSupportedException) as e:
        sys.stderr.write('error:'+str(e)+'\n')


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
