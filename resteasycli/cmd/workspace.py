import json
from cliff.show import ShowOne
from cliff.lister import Lister
from resteasycli.objects import workspace


class ListSites(Lister):
    '''List available sites in current workspace'''
    def take_action(self, args):
        result = workspace.list_sites()
        return [['site', 'base_url'], result.items()]

class ListEndpoints(Lister):
    '''List available endpoints in current workspace'''
    def take_action(self, args):
        result = workspace.list_endpoints()
        return [['site_endpoint', 'endpoint_url'], result.items()]

class ListSavedRequests(Lister):
    '''List all saved requests in current workspace'''
    def take_action(self, args):
        result = workspace.list_saved_requests()
        header = ['request', 'method', 'site_endpoint', 'kwargs']
        body = []
        for k, v in result.items():
            body.append([k, v['method'], v['site_endpoint'], json.dumps(v['kwargs'], indent=2)])
        return [header, body]

class ShowSavedRequest(ShowOne):
    '''Show a particular saved request'''
    def get_parser(self, prog_name):
        parser = super(ShowSavedRequest, self).get_parser(prog_name)
        parser.add_argument('saved_request')
        return parser

    def take_action(self, args):
        result = workspace.list_saved_requests().get(args.saved_request)
        if result is None:
            raise RuntimeError('error: {}: saved request not found'.format(args.saved_request))
        if 'kwargs' in result:
            result['kwargs'] = json.dumps(result['kwargs'], indent=2)
        
        if 'headers_values' in result:
            result['headers_values'] = (
                '; '.join(['{}: {}'.format(k, v) for k, v in result['headers_values'].items()]))
        return [result.keys(), result.values()]
