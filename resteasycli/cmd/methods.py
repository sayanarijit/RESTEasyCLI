import sys
import json
from abc import ABC
from cliff.show import ShowOne
from cliff.lister import Lister

from cliff.command import Command
from resteasycli.logger import logger
from resteasycli.lib.site import Site
from resteasycli.lib.abstract_reader import Reader
from resteasycli.lib.abstract_finder import Finder
from resteasycli.exceptions import InvalidEndpointException

finder = Finder(logger=logger)
found = finder.find(names=['sites'])
reader = Reader(logger=logger)
reader.load_reader_by_extension(found.extension)
data = reader.read(found.path)


class GenericRequest(Command, ABC):
    '''Generic interface for API requests'''
    def get_parser(self, prog_name):
        parser = super(GenericRequest, self).get_parser(prog_name)
        parser.add_argument('endpoint')
        parser.add_argument('-k', '--kwargs', type=str, nargs='*')
        parser.add_argument('-t', '--timeout', type=int)
        return parser

    @staticmethod
    def parse_kwargs(lst):
        if lst is None:
            return {}
        return {x.split('=', 1)[0]: x.split('=', 1)[1] for x in lst}

    def do(self, args):
        if len(args.endpoint.split('/')) == 2:
            slug = None
            site_name, endpoint_name = args.endpoint.split('/')
        elif len(args.endpoint.split('/')) == 3:
            site_name, endpoint_name, slug = args.endpoint.split('/')
        else:
            raise InvalidEndpointException(
                'correct format of endpoint is: $site/$endpoint or $site/$endpoint/$slug')
        site = Site(data['sites'][site_name])
        endpoint = site.get_endpoint(
            data['sites'][site_name]['endpoints'][endpoint_name], slug=slug)
        if args.timeout is not None:
            endpoint.api.timeout = args.timeout
        return endpoint.do(self.METHOD, kwargs=self.parse_kwargs(args.kwargs))
    
    def take_action(self, args):
        sys.stdout.write(json.dumps(self.do(args), indent=4))

class GET(GenericRequest):
    '''Do GET request'''
    METHOD = 'GET'

class POST(GenericRequest):
    '''Do POST request'''
    METHOD = 'POST'

class PUT(GenericRequest):
    '''Do PUT request'''
    METHOD = 'PUT'

class PATCH(GenericRequest):
    '''Do PATCH request'''
    METHOD = 'PATCH'

class DELETE(GenericRequest):
    '''Do DELETE request'''
    METHOD = 'DELETE'

class LIST(GenericRequest, Lister):
    '''Fetch a list of results'''

    METHOD = 'GET'

    def take_action(self, args):
        data = self.do(args)
        if len(data) == 0:
            return []
        if isinstance(data, dict):
            raise RuntimeError('error: use `show` method instead')
        header = data[0].keys()
        body = [x.values() for x in data]
        return [header, body]

class SHOW(GenericRequest, ShowOne):
    '''SHOW a particular result'''

    METHOD = 'GET'
    
    def take_action(self, args):
        data = self.do(args)
        if len(data) == 0:
            return {}
        if isinstance(data, list):
            raise RuntimeError('error: use `list` method instead')
        return [data.keys(), data.values()]
