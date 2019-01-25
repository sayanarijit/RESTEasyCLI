import logging
from cliff.command import Command

from resteasycli.lib.doc import APIDocument


class Generate(Command):
    'Auto generate API docs from workspace files'

    def get_parser(self, prog_name):
        parser = super(Generate, self).get_parser(prog_name)
        parser.add_argument('filepath', help='file path for the document')
        parser.add_argument('-H', '--hide_cred', action='store_true')
        return parser

    def take_action(self, args):
        doc = APIDocument(self.app.workspace, hide_cred=args.hide_cred)
        doc.dump(args.filepath)
