import sys
import json
import yaml
from cliff.show import ShowOne
from cliff.lister import Lister

from resteasycli.objects import workspace
from resteasycli.exceptions import InvalidCommandException


class RequestFactory(object):
    '''Helps producing unformatted request commands'''

    @staticmethod
    def write_output(data, fmt):
        '''Write data to stdout'''

        if fmt == 'json':
            out = json.dumps(data, indent=2)
        else:
            out = yaml.dump(data, default_flow_style=False)
        sys.stdout.write(out+'\n')

    @staticmethod
    def unformatted(parent_class):
        '''Builds and returns the class for unformatted request'''


        class UnformattedRequest(parent_class):
            '''Parent for CRUD operation with unformatted outputs'''

            def get_parser(self, prog_name):
                '''Add custom formats'''
                parser = super(UnformattedRequest, self).get_parser(prog_name)
                parser.add_argument(
                    '-f', '--format',
                    choices=workspace.config.SUPPORTED_OUTPUT_FORMATS,
                    default=workspace.config.DEFAULT_OUTPUT_FORMAT,
                    help='the output format')
                return parser

            def act(self, method, args):
                '''Act based on request method and args'''
                req = self.get_request(method, args)
                resp = self.get_response(req, args)
                RequestFactory.write_output(resp, fmt=args.format)
        return UnformattedRequest

    @staticmethod
    def listformatted(parent_class):
        '''Builds and returns the class for list formatted request'''

        class ListFormattedRequest(Lister, parent_class):
            '''Parent class for requests with list formatted outputs'''

            def act(self, method, args):
                '''Act based on request method and args'''
                req = self.get_request(method, args)
                resp = self.get_response(req, args)

                if args.fake:
                    return [resp.keys(), [[dict(x) for x in resp.values()]]]

                if len(resp) == 0:
                    return [[], []]
                if isinstance(resp, dict):
                    raise InvalidCommandException('use `show`/`redo-show` operation instead')
                header = resp[0].keys()
                body = [x.values() for x in resp]
                return [header, body]

        return ListFormattedRequest

    @staticmethod
    def showoneformatted(parent_class):
        '''Builds and returns the class for table formatted request'''

        class ShowOneFormattedRequest(ShowOne, parent_class):
            '''Parent class for requests with list formatted outputs'''
            def act(self, method, args):
                '''Act based on request method and args'''
                req = self.get_request(method, args)
                resp = self.get_response(req, args)

                if args.fake:
                    return [resp.keys(), [dict(x) for x in resp.values()]]

                if len(resp) == 0:
                    return [[], []]
                if isinstance(resp, list):
                    raise InvalidCommandException('use `list`/`redo-list` operation instead')
                return [resp.keys(), resp.values()]

        return ShowOneFormattedRequest
