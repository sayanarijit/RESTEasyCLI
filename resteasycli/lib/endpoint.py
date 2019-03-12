from collections import OrderedDict
from resteasy import requests

from resteasycli.exceptions import MethodNotAllowedException


requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning,
)


class Endpoint(object):
    '''Holds endpoint of a site'''

    def __init__(self, endpoint_id, site, slug=None):
        data = site.endpoints[endpoint_id]
        self.endpoint_id = endpoint_id
        self.site = site
        self.logger = site.logger
        self.api = self.site.route(data['route'])
        self.auth_applied = site.auth_applied
        self.headers_applied = site.headers_applied
        self.timeout_applied = site.timeout_applied
        self.verify_applied = site.verify_applied
        self.allowed_methods = site.allowed_methods
        self.allowed_methods_applied = site.allowed_methods_applied
        if slug is not None:
            self.api = self.api.route(slug)
        if 'auth' in data:
            self.auth_applied = site.workspace.get_auth(data['auth'])
            self.auth_applied.apply(self.api.session)
        if 'headers' in data:
            self.headers_applied = site.workspace.get_headers(data['headers'])
            self.headers_applied.apply(self.api.session)
        if 'timeout' in data:
            self.timeout_applied = data['timeout']
            self.api.timeout = data['timeout']
        if 'verify' in data:
            self.verify_applied = data['verify']
            self.api.session.verify = data['verify']
        if 'methods' in data:
            self.allowed_methods = list(
                map(lambda x: x.upper(), data['methods']),
            )
            self.allowed_methods_applied = self.allowed_methods

    def do(self, method, kwargs={}):
        '''Do the request'''

        if method not in self.allowed_methods and not self.api.debug:
            raise MethodNotAllowedException(
                'allowed methods are: ' + (', '.join(self.allowed_methods)),
            )

        return self.api.do(method, kwargs)

    def dict(self):
        '''Return information about itself in dict format'''
        data = OrderedDict([('endpoint_url', self.api.endpoint)])
        if self.auth_applied is not None:
            data['auth'] = self.auth_applied.auth_id
        if self.headers_applied is not None:
            data['headers'] = self.headers_applied.headers_id
        if self.timeout_applied is not None:
            data['timeout'] = self.timeout_applied
        if self.verify_applied is not None:
            data['verify'] = self.verify_applied
        if self.allowed_methods_applied is not None:
            data['allowed_methods'] = self.allowed_methods_applied
        return data
