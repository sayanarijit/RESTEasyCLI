import json
from cliff.show import ShowOne
from cliff.lister import Lister
from resteasycli.objects import workspace
from resteasycli.exceptions import InvalidCommandException


class ListSites(Lister):
    '''List available sites in current workspace'''
    def take_action(self, args):
        result =  {k: v['base_url'] for k,v in workspace.sites.items()}
        return [['site', 'base_url'], result.items()]

class ShowSite(ShowOne):
    '''Show information about a site'''
    def get_parser(self, prog_name):
        parser = super(ShowSite, self).get_parser(prog_name)
        parser.add_argument('site_id')
        return parser

    def take_action(self, args):
        result = workspace.get_site(args.site_id).dict()
        return [result.keys(), result.values()]

class ListEndpoints(Lister):
    '''List available endpoints in current workspace'''
    def take_action(self, args):
        result = {}
        for site, values in workspace.sites.items():
            base_url = values['base_url']
            for endpoint, values in values['endpoints'].items():
                result['{}/{}'.format(site, endpoint)] = '{}/{}'.format(base_url, values['route'])
        return [['site_endpoint', 'endpoint_url'], result.items()]

class ShowEndpoint(ShowOne):
    '''Show information about an endpoint'''
    def get_parser(self, prog_name):
        parser = super(ShowEndpoint, self).get_parser(prog_name)
        parser.add_argument('site_endpoint')
        return parser

    def take_action(self, args):
        if len(args.site_endpoint.split('/')) != 2:
            raise InvalidCommandException(
                    '{}: correct format is: $site_id/$endpoint_id'.format(args.site_endpoint))
        site_id, endpoint_id = args.site_endpoint.split('/')
        site = workspace.get_site(site_id)
        result = site.get_endpoint(endpoint_id).dict()
        return [result.keys(), result.values()]

class ListSavedRequests(Lister):
    '''List all saved requests in current workspace'''
    def take_action(self, args):
        result = workspace.saved_requests
        header = ['request', 'method', 'site_endpoint']
        body = []
        for k, v in result.items():
            site_endpoint = '{}/{}'.format(v['site'], v['endpoint'])
            body.append([k, v['method'], site_endpoint])
        return [header, body]

class ShowSavedRequest(ShowOne):
    '''Show a particular saved request'''
    def get_parser(self, prog_name):
        parser = super(ShowSavedRequest, self).get_parser(prog_name)
        parser.add_argument('request_id')
        return parser

    def take_action(self, args):
        result = workspace.get_saved_request(args.request_id).dict()
        return [result.keys(), result.values()]

class ListHeaders(Lister):
    '''List all headers in current workspace'''
    def take_action(self, args):
        result = workspace.headers
        header = ['headers_id', 'action', 'values']
        body = []
        for k, v in result.items():
            body.append([k, v['action'], '\n'.join(['{}: {}'.format(x,y) for x,y in v['values'].items()])])
        return [header, body]

class ShowHeaders(ShowOne):
    '''Show a particular set of headers'''
    def get_parser(self, prog_name):
        parser = super(ShowHeaders, self).get_parser(prog_name)
        parser.add_argument('headers_id')
        return parser

    def take_action(self, args):
        result = workspace.get_headers(args.headers_id).dict()
        return [result.keys(), result.values()]

class ListAuth(Lister):
    '''List all authentication methods in current workspace'''
    def take_action(self, args):
        result = workspace.auth
        header = ['auth_id', 'type', 'credentials']
        body = []
        for k, v in result.items():
            body.append([k, v['type'], v['credentials']])
        return [header, body]

class ShowAuth(ShowOne):
    '''Show a particular authentication method'''
    def get_parser(self, prog_name):
        parser = super(ShowAuth, self).get_parser(prog_name)
        parser.add_argument('auth_id')
        return parser

    def take_action(self, args):
        result = workspace.get_auth(args.auth_id).dict()
        return [result.keys(), result.values()]

