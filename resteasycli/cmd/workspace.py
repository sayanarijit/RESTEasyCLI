from cliff.show import ShowOne
from cliff.lister import Lister
from resteasycli.cmd.common import SiteEndpoint
from resteasycli.exceptions import InvalidCommandException


class ListSites(Lister):
    '''List available sites in current workspace'''

    def take_action(self, args):
        result = [(k, v['base_url']) for k, v in self.workspace.sites.items()]
        return [['site', 'base_url'], result]


class ShowSite(ShowOne):
    '''Show information about a site'''

    def get_parser(self, prog_name):
        parser = super(ShowSite, self).get_parser(prog_name)
        parser.add_argument('site_id', choices=self.workspace.sites.keys())
        return parser

    def take_action(self, args):
        result = self.workspace.get_site(args.site_id).dict()
        return [result.keys(), result.values()]


class ListEndpoints(Lister):
    '''List available endpoints in current workspace'''

    def take_action(self, args):
        result = []
        for site, values in self.workspace.sites.items():
            base_url = values['base_url']
            for endpoint, values in values['endpoints'].items():
                result.append((
                    '{}/{}'.format(site, endpoint),
                    '{}/{}'.format(base_url, values['route'])
                ))
        return [['site_endpoint', 'endpoint_url'], result]


class ShowEndpoint(ShowOne):
    '''Show information about an endpoint'''

    def get_parser(self, prog_name):
        parser = super(ShowEndpoint, self).get_parser(prog_name)
        choices = []
        ds = self.workspace.config.DEFAULT_SITE_ID
        dep = self.workspace.config.DEFAULT_ENDPOINT_ID

        if ds in self.workspace.sites:
            if dep in self.workspace.sites[ds]['endpoints']:
                choices.append(SiteEndpoint('/'))
            choices += list(map(
                lambda x: SiteEndpoint('/'+x),
                self.workspace.sites[ds]['endpoints'].keys()))

        for s, v in self.workspace.sites.items():
            if dep in v['endpoints']:
                choices.append(SiteEndpoint(s+'/'))
            for e in v['endpoints'].keys():
                choices.append(SiteEndpoint('{}/{}'.format(s, e)))

        parser.add_argument('target', type=SiteEndpoint, choices=choices)
        return parser

    def take_action(self, args):
        site_id = args.target.site_id
        endpoint_id = args.target.endpoint_id

        if not site_id:
            if self.workspace.config.DEFAULT_SITE_ID:
                site_id = self.workspace.config.DEFAULT_SITE_ID
            else:
                raise InvalidCommandException('default site ID is not defined')

        if not endpoint_id:
            if self.workspace.config.DEFAULT_ENDPOINT_ID:
                endpoint_id = self.workspace.config.DEFAULT_ENDPOINT_ID
            else:
                raise InvalidCommandException('default endpoint ID is not defined')

        site = self.workspace.get_site(site_id)
        result = site.get_endpoint(endpoint_id).dict()
        return [result.keys(), result.values()]


class ListSavedRequests(Lister):
    '''List all saved requests in current workspace'''
    def take_action(self, args):
        result = self.workspace.saved_requests
        header = ['request', 'method', 'site_endpoint']
        body = []
        for k, v in result.items():
            site_endpoint = '{}/{}'.format(v['site'], v['endpoint'])
            body.append((k, v['method'], site_endpoint))
        return [header, body]


class ShowSavedRequest(ShowOne):
    '''Show a particular saved request'''
    def get_parser(self, prog_name):
        parser = super(ShowSavedRequest, self).get_parser(prog_name)
        parser.add_argument('request_id', choices=self.workspace.saved_requests.keys())
        return parser

    def take_action(self, args):
        result = self.workspace.get_saved_request(args.request_id).dict()
        return [result.keys(), result.values()]


class ListHeaders(Lister):
    '''List all headers in current workspace'''
    def take_action(self, args):
        result = self.workspace.headers
        header = ['headers_id', 'action', 'values']
        body = []
        for k, v in result.items():
            body.append((
                k, v['action'], '\n'.join([
                    '{}: {}'.format(x, y) for x, y in v['values'].items()])
            ))
        return [header, body]


class ShowHeaders(ShowOne):
    '''Show a particular set of headers'''
    def get_parser(self, prog_name):
        parser = super(ShowHeaders, self).get_parser(prog_name)
        parser.add_argument('headers_id', choices=self.workspace.headers.keys())
        return parser

    def take_action(self, args):
        result = self.workspace.get_headers(args.headers_id).dict()
        return [result.keys(), result.values()]


class ListAuth(Lister):
    '''List all authentication methods in current workspace'''
    def take_action(self, args):
        result = self.workspace.auth
        header = ['auth_id', 'type']
        body = []
        for k, v in result.items():
            body.append((k, v['type']))
        return [header, body]


class ShowAuth(ShowOne):
    '''Show a particular authentication method'''
    def get_parser(self, prog_name):
        parser = super(ShowAuth, self).get_parser(prog_name)
        parser.add_argument('auth_id', choices=self.workspace.auth.keys())
        return parser

    def take_action(self, args):
        result = self.workspace.get_auth(args.auth_id).dict()
        return [result.keys(), result.values()]

