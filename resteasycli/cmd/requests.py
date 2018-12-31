import sys
import json
from cliff.show import ShowOne
from cliff.lister import Lister
from cliff.command import Command

from resteasycli.objects import workspace
from resteasycli.lib.request import Request


class List(Lister):
    '''Fetch a list of resources'''

    def take_action(self, args):
        request = self.get_request('GET', args)
        if args.save_as is not None:
            request.save_as(args.save_as)
        if args.fake:
            self.dump_json(request.dict())
            return [[], []]

        data = request.do()
        if len(data) == 0:
            return [[], []]
        if isinstance(data, dict):
            raise RuntimeError('error: use `show`/`redo-show` operation instead')
        header = data[0].keys()
        body = [x.values() for x in data]
        return [header, body]

class Show(ShowOne):
    '''Show a particular resource'''

    def take_action(self, args):
        request = self.get_request('GET', args)
        if args.save_as is not None:
            request.save_as(args.save_as)
        if args.fake:
            self.dump_json(request.dict())
            return [[], []]

        data = request.do()
        if len(data) == 0:
            return [[], []]
        if isinstance(data, list):
            raise RuntimeError('error: use `list`/`redo-list` operation instead')
        return [data.keys(), data.values()]


class GenericRequest(Command):
    '''The generic request class for all requests'''

    def get_parser(self, prog_name):
        parser = super(GenericRequest, self).get_parser(prog_name)
        parser.add_argument('-m', '--method', help='override query method')
        parser.add_argument('-k', '--kwargs', type=str, nargs='*',
                            help='set kwargs by removing old one')
        parser.add_argument('-u', '--update_kwargs', type=str, nargs='*',
                            help='update only mentioned key-value pairs')
        parser.add_argument(
            '-a', '--auth', help='use alternate authentication from file')
        parser.add_argument('-H', '--headers',
                            help='use alternate set of headers from file')
        parser.add_argument('-t', '--timeout', type=int)
        parser.add_argument('-F', '--fake', help='print the request instead of actually doing it',
                            action='store_true')
        parser.add_argument('-s', '--save_as',
                            help='save the request for later use. can be used with --fake option')
        return parser

    @staticmethod
    def parse_kwargs(lst):
        if lst is None:
            return {}
        return {x.split('=', 1)[0]: x.split('=', 1)[1] for x in lst}

    def get_request(self, method, site_id, endpoint_id, args):
        '''get the request object'''

        request = Request(workspace=workspace, method=method,
                site_id=site_id, endpoint_id=endpoint_id)

        if args.timeout is not None:
            request.set_timeout(args.timeout)

        if args.kwargs is not None:
            request.set_kwargs(GenericRequest.parse_kwargs(args.kwargs))

        if args.update_kwargs is not None:
            request.update_kwargs(GenericRequest.parse_kwargs(args.update_kwargs))

        if args.auth is not None:
            request.set_auth(args.auth)

        if args.headers is not None:
            request.set_headers(args.headers)

        if args.slug is not None:
            request.add_slug(args.slug)

        if args.fake:
            request.set_debug(True)

        if args.save_as is not None:
            request.save_as(request_id=args.save_as)

        return request

    def act(self, args):
        request = self.get_request(args)
        if args.save_as is not None:
            request.save_as(args.save_as)
        if args.fake:
            self.dump_json(request.dict())
        else:
            self.dump_json(request.do())

    @staticmethod
    def dump_json(data):
        sys.stdout.write(json.dumps(data, indent=2)+'\n')


class UnSavedRequest(GenericRequest):
    '''New  interface for API requests'''
    def get_parser(self, prog_name):
        parser = super(UnSavedRequest, self).get_parser(prog_name)
        parser.add_argument('site_endpoint',
                            help='format: $site/$endpoint or $site_id/$endpoint_id/$slug')
        return parser

    def get_request(self, method, args):
        '''Build and get the request object'''
        if len(args.site_endpoint.split('/')) == 2:
            args.slug = None
            site_id, endpoint_id = args.site_endpoint.split('/')
        elif len(args.site_endpoint.split('/')) == 3:
            site_id, endpoint_id, args.slug = args.site_endpoint.split('/')
        else:
            raise RuntimeError(
                'error: {}: correct format of endpoint is: $site_id/$endpoint_id or $site_id/$endpoint_id/$slug'.format(args.site_endpoint))
        return super(UnSavedRequest, self).get_request(method=method, site_id=site_id,
                endpoint_id=endpoint_id, args=args)

    def take_action(self, args):
        self.act(args)

class GET(UnSavedRequest):
    '''Do GET request'''
    def get_request(self, args):
        return super(GET, self).get_request(method='GET', args=args)


class POST(UnSavedRequest):
    '''Do POST request'''
    def get_request(self, args):
        return super(POST, self).get_request(method='POST', args=args)

class PUT(UnSavedRequest):
    '''Do PUT request'''
    def get_request(self, args):
        return super(PUT, self).get_request(method='PUT', args=args)

class PATCH(UnSavedRequest):
    '''Do PATCH request'''
    def get_request(self, args):
        return super(PATCH, self).get_request(method='PATCH', args=args)

class DELETE(UnSavedRequest):
    '''Do DELETE request'''
    def get_request(self, args):
        return super(DELETE, self).get_request(method='DELETE', args=args)

class UnSavedList(List, UnSavedRequest):
    '''Fetch a list of resources'''
    pass

class UnSavedShow(Show, UnSavedRequest):
    '''Show a particular resource'''
    pass


class SavedRequest(GenericRequest):
    '''Generic saved request API'''

    def get_parser(self, prog_name):
        parser = super(SavedRequest, self).get_parser(prog_name)
        parser.add_argument('request_id', help='request ID from saved requests')
        parser.add_argument('-S', '--slug', help='add slug to the endpoint')
        return parser

    def get_request(self, method, args):
        '''Build and get the request object'''

        if args.request_id not in workspace.saved_requests:
            raise RuntimeError(
                'error: {}: request ID not found'.format(args.request_id))

        request = workspace.get_saved_request(args.request_id)

        method = args.method if args.method is not None else request.method

        return super(SavedRequest, self).get_request(method=method,
                site_id=request.endpoint.site.site_id, endpoint_id=request.endpoint.endpoint_id, args=args)

    def take_action(self, args):
        self.act(args)

class SavedRedo(SavedRequest):
    '''Re-do a saved request'''
    def get_request(self, args):
        return super(SavedRedo, self).get_request(method=args.method, args=args)

class SavedShow(Show, SavedRequest):
    '''Re-do show operation on saved requests for formatted outputs'''
    pass

class SavedList(List, SavedRequest):
    '''Re-do list operation on saved requests for formatted outputs'''
    pass
