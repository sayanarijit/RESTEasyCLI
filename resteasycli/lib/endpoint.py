from resteasy import APIEndpoint
from resteasy import requests

from resteasycli.config import Config
from resteasycli.exceptions import MethodNotAllowedException


requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)


class Endpoint(object):
    '''Holds endpoint of a site'''

    def __init__(self, endpoint_id, site, slug=None):
        data = site.endpoints[endpoint_id]
        self.site = site
        self.api = APIEndpoint(endpoint=('{}/{}'.format(site.base_url, data['route'])),
                session=site.session,
                timeout=site.timeout, debug=site.debug)
        if slug is not None:
            self.api = self.api.route(slug)
        if 'auth' in data:
            site.workspace.get_auth(data['auth']).apply(self.api.session)
        if 'headers' in data:
            site.workspace.get_headers(data['headers']).apply(self.api.session)
        if 'timeout' in data:
            self.api.timeout = data['timeout']
        self.allowed_methods = Config.DEFAULT_ALLOWED_METHODS
        if 'methods' in data:
            self.allowed_methods = list(map(lambda x: x.upper(), data['methods']))
    
    def do(self, method, kwargs={}, slug=None):
        if method not in self.allowed_methods:
            raise MethodNotAllowedException('allowed methods are: ' + (', '.join(self.allowed_methods)))

        return self.api.do(method, kwargs)
