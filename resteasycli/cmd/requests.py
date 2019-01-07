import sys
import json
from cliff.show import ShowOne
from cliff.lister import Lister
from cliff.command import Command

from resteasycli.objects import workspace
from resteasycli.lib.request import Request
from resteasycli.exceptions import InvalidCommandException


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
            raise InvalidCommandException('use `show`/`redo-show` operation instead')
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
            raise InvalidCommandException('use `list`/`redo-list` operation instead')
        return [data.keys(), data.values()]


class GenericRequest(Command):
    '''The generic request class for all requests'''

    def get_parser(self, prog_name):
        parser = super(GenericRequest, self).get_parser(prog_name)
        parser.add_argument('-m', '--method', help='override query method')
        parser.add_argument('-k', '--kwargs', type=self.parse_kwarg, nargs='*',
                help='payload/params to send. format: key1=value "key2=another value"')
        parser.add_argument('-u', '--update_kwargs', type=self.parse_kwarg, nargs='*',
                help='add/update key-value pairs in kwargs. format: key1=value "key2=another value"')
        parser.add_argument(
                '-a', '--auth', help='use alternate authentication from file',
                default=workspace.config.DEFAULT_AUTH_ID)
        parser.add_argument('-H', '--headers',
                help='use alternate set of headers from file',
                default=workspace.config.DEFAULT_HEADERS_ID)
        parser.add_argument('-t', '--timeout', type=int,
                default=workspace.config.DEFAULT_TIMEOUT)
        parser.add_argument('-C', '--certfile', help='ssl certificate file path',
                default=workspace.config.DEFAULT_CERTFILE)
        parser.add_argument('-I', '--insecure', action='store_true',
                help='do not verify ssl certificate. (overrides "-C", "--certfile" option)')
        parser.add_argument('-F', '--fake', help='print the request instead of actually doing it',
                action='store_true')
        parser.add_argument('-s', '--save_as',
                help='save the request for later use. can be used with --fake option')
        return parser

    @staticmethod
    def parse_kwarg(pair):
        try:
            return {pair.split('=', 1)[0]: pair.split('=', 1)[1]}
        except Exception:
            raise InvalidCommandException('kwargs: correct format is: key1=value "key2=another value"')

    @staticmethod
    def parse_kwargs(lst):
        if lst is None:
            return None
        data = {}
        for kv in lst: data.update(kv)
        return data

    def get_request(self, method, site_id, endpoint_id, args, request=None):
        '''get the request object'''

        # Check if endpoint extsts
        site = workspace.get_site(site_id)
        endpoint = site.get_endpoint(endpoint_id)

        if request is None:
            request = Request(workspace=workspace, method=method,
                    site_id=site.site_id, endpoint_id=endpoint.endpoint_id)
        else:
            request.set_method(method)

        if args.timeout is not None:
            request.set_timeout(args.timeout)

        if args.kwargs is not None:
            request.set_kwargs(self.parse_kwargs(args.kwargs))

        if args.update_kwargs is not None:
            request.update_kwargs(self.parse_kwargs(args.update_kwargs))

        if args.auth is not None:
            request.set_auth(args.auth)

        if args.headers is not None:
            request.set_headers(args.headers)

        if args.certfile is not None:
            request.set_verify(args.certfile)

        if args.insecure:
            request.set_verify(False)

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
                            help='format: $site_id/$endpoint_id or $site_id/$endpoint_id/$slug')
        return parser

    def get_request(self, method, args):
        '''Build and get the request object'''
        if len(args.site_endpoint.split('/')) == 2:
            args.slug = None
            site_id, endpoint_id = args.site_endpoint.split('/')
        elif len(args.site_endpoint.split('/')) > 2:
            site_id, endpoint_id, args.slug = args.site_endpoint.split('/', 2)
        else:
            raise InvalidCommandException(
                '{}: correct format of endpoint is: $site_id/$endpoint_id or $site_id/$endpoint_id/$slug'.format(args.site_endpoint))

        if not site_id:
            if workspace.config.DEFAULT_SITE_ID:
                site_id = workspace.config.DEFAULT_SITE_ID
            else:
                raise InvalidCommandException('default site ID is not defined')

        if not endpoint_id:
            if workspace.config.DEFAULT_ENDPOINT_ID:
                endpoint_id = workspace.config.DEFAULT_ENDPOINT_ID
            else:
                raise InvalidCommandException('default endpoint ID is not defined')

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

        request = workspace.get_saved_request(args.request_id)

        method = args.method if args.method is not None else request.method

        return super(SavedRequest, self).get_request(method=method, site_id=request.endpoint.site.site_id,
                endpoint_id=request.endpoint.endpoint_id, args=args, request=request)

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
