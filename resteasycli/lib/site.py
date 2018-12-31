from resteasy import RESTEasy

from resteasycli.config import Config
from resteasycli.lib.endpoint import Endpoint

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
        return Endpoint(endpoint_id=endpoint_id, site=self, slug=slug)
