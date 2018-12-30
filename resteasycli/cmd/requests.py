import sys
import json
from cliff.show import ShowOne
from cliff.lister import Lister
from cliff.command import Command

from resteasycli.objects import workspace
from resteasycli.exceptions import InvalidEndpointException


class GenericRequest(Command):
    '''Generic interface for API requests'''
    def get_parser(self, prog_name):
        parser = super(GenericRequest, self).get_parser(prog_name)
        parser.add_argument('site_endpoint',
                            help='format: $site/$endpoint or $site_id/$endpoint_id/$slug')
        parser.add_argument('-k', '--kwargs', type=str, nargs='*')
        parser.add_argument('-t', '--timeout', type=int)
        parser.add_argument('-F', '--fake', action='store_true')
        return parser

    @staticmethod
    def parse_kwargs(lst):
        if lst is None:
            return {}
        return {x.split('=', 1)[0]: x.split('=', 1)[1] for x in lst}

    def do(self, args):
        if len(args.site_endpoint.split('/')) == 2:
            slug = None
            site_id, endpoint_id = args.site_endpoint.split('/')
        elif len(args.site_endpoint.split('/')) == 3:
            site_id, endpoint_id, slug = args.site_endpoint.split('/')
        else:
            raise InvalidEndpointException(
                'error: {}: correct format of endpoint is: $site_id/$endpoint_id or $site_id/$endpoint_id/$slug'.format(args.site_endpoint))
        
        endpoint = workspace.get_site(site_id).get_endpoint(endpoint_id, slug=slug)

        if args.timeout is not None:
            endpoint.api.timeout = args.timeout

        if args.fake:
            endpoint.api.debug = True

        return endpoint.do(self.METHOD, kwargs=self.parse_kwargs(args.kwargs))
    
    def take_action(self, args):
        result = self.do(args)
        if args.fake:
            del result['session']
        sys.stdout.write(json.dumps(result, indent=4)+'\n')

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

class List(GenericRequest, Lister):
    '''Fetch a list of resources'''

    METHOD = 'GET'

    def take_action(self, args):
        data = self.do(args)
        if len(data) == 0:
            return []
        if isinstance(data, dict):
            raise RuntimeError('error: use `show` operation instead')
        header = data[0].keys()
        body = [x.values() for x in data]
        return [header, body]

class Show(GenericRequest, ShowOne):
    '''Show a particular resource'''

    METHOD = 'GET'

    def take_action(self, args):
        data = self.do(args)
        if args.fake:
            del data['session']
        if len(data) == 0:
            return {}
        if isinstance(data, list):
            raise RuntimeError('error: use `list` operation instead')
        return [data.keys(), data.values()]


class ReDoQueryFromSavedRequests(GenericRequest):
    '''Re-do query from saved requests'''

    def get_parser(self, prog_name):
        parser = super(GenericRequest, self).get_parser(prog_name)
        parser.add_argument(
            'request_id', help='mention the request ID from saved requests')
        parser.add_argument('-m', '--method', help='override query method')
        parser.add_argument('-k', '--kwargs', type=str, nargs='*',
                            help='set kwargs by removing old one')
        parser.add_argument('-u', '--update_kwargs', type=str, nargs='*',
                            help='update only mentioned key-value pairs')
        parser.add_argument('-a', '--auth_id', help='use alternate authentication from file')
        parser.add_argument('-x', '--headers_id', help='use alternate set of headers from file')
        parser.add_argument('-s', '--slug', help='add a slug to existing endpoint')
        parser.add_argument('-t', '--timeout', type=int)
        parser.add_argument('-F', '--fake', action='store_true')
        return parser

    def do(self, args):
        if args.request_id not in workspace.saved_requests:
            raise RuntimeError('error: {}: request ID not found'.format(args.request_id))

        request = workspace.get_saved_request(args.request_id)

        if args.method is not None:
            request.set_method(args.method)

        if args.timeout is not None:
            request.set_timeout(args.timeout)

        if args.kwargs is not None:
            request.set_kwargs(self.parse_kwargs(args.kwargs))
        
        if args.update_kwargs is not None:
            request.update_kwargs(self.parse_kwargs(args.update_kwargs))

        if args.auth_id is not None:
            request.set_auth(args.auth_id)
        
        if args.headers_id is not None:
            request.set_headers(args.headers_id)
        
        if args.slug is not None:
            request.add_slug(args.slug)
        
        if args.fake:
            request.set_debug(True)
        
        return request.do()


class ReDoListFromSavedRequest(ReDoQueryFromSavedRequests, List):
    '''Re-do list operation on saved requests for formatted outputs'''

    def take_action(self, args):
        args.method = 'GET'
        data = self.do(args)
        if len(data) == 0:
            return []
        if isinstance(data, dict):
            raise RuntimeError('error: use `redo-show` operation instead')
        header = data[0].keys()
        body = [x.values() for x in data]
        return [header, body]


class ReDoShowFromSavedRequest(ReDoQueryFromSavedRequests, Show):
    '''Re-do list operation on saved requests for formatted outputs'''

    def take_action(self, args):
        args.method = 'GET'
        data = self.do(args)
        if args.fake:
            del data['session']

        if len(data) == 0:
            return {}
        if isinstance(data, list):
            raise RuntimeError(
                'error: use `redo-list` operation instead')
        return [data.keys(), data.values()]
