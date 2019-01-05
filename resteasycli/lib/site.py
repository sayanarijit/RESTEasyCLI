from resteasy import RESTEasy
from collections import OrderedDict

from resteasycli.config import Config
from resteasycli.lib.endpoint import Endpoint
from resteasycli.exceptions import EntryNotFoundException


class Site(RESTEasy):
    '''A site is a modified RESTEasy object'''
    def __init__(self, site_id, workspace):
        data = workspace.sites[site_id]
        RESTEasy.__init__(self, base_url=data['base_url'])
        self.site_id = site_id
        self.logger = workspace.logger
        self.workspace = workspace
        self.endpoints = data['endpoints']
        self.auth_applied = None
        self.headers_applied = None
        self.timeout_applied = None
        self.verify_applied = None
        self.allowed_methods = Config.DEFAULT_ALLOWED_METHODS
        self.allowed_methods_applied = None
        if 'auth' in data:
            self.auth_applied = workspace.get_auth(data['auth'])
            self.auth_applied.apply(self.session)
        if 'headers' in data:
            self.headers_applied = workspace.get_headers(data['headers'])
            self.headers_applied.apply(self.session)
        if 'verify' in data:
            self.verify_applied = data['verify']
            self.session.verify = data['verify']
        if 'timeout' in data:
            self.timeout_applied = data['timeout']
            self.timeout = data['timeout']
        if 'methods' in data:
            self.allowed_methods = list(
                map(lambda x: x.upper(), data['methods']))
            self.allowed_methods_applied = self.allowed_methods

    def get_endpoint(self, endpoint_id, slug=None):
        '''Return an initialized endpoint object'''
        if endpoint_id not in self.endpoints:
            raise EntryNotFoundException('{}: endpoint not found'.format(endpoint_id))
        return Endpoint(endpoint_id=endpoint_id, site=self, slug=slug)

    def dict(self):
        '''Return information about itself in dict format'''
        data = OrderedDict([
            ('endpoints', list(self.endpoints.keys())),
            ('base_url', self.base_url)
        ])
        if self.auth_applied is not None:
            data.update({'auth': self.auth_applied.auth_id})
        if self.headers_applied is not None:
            data.update({'headers': self.headers_applied.headers_id})
        if self.timeout_applied is not None:
            data.update({'timeout': self.timeout_applied})
        if self.verify_applied is not None:
            data.update({'verify': self.verify_applied})
        if self.allowed_methods_applied is not None:
            data.update({'allowed_methods': self.allowed_methods_applied})
        return data
