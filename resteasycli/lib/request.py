import time
from resteasycli.lib.locked_read_writer import LockedReadWriter


class Request(object):
    '''A generic request'''

    def __init__(self, workspace, method, site_id, endpoint_id, **data):
        self.workspace = workspace
        self.method = method
        self.endpoint = workspace.get_site(site_id).get_endpoint(endpoint_id)
        self.kwargs = data.get('kwargs', {})
        self.auth_applied = None
        self.headers_applied = None
        self.timeout_applied = None
        self.verify_applied = None
        if 'auth' in data:
            self.auth_applied = workspace.get_auth(data['auth'])
            self.auth_applied.apply(self.endpoint.api.session)
        if 'headers' in data:
            self.headers_applied = workspace.get_headers(data['headers'])
            self.headers_applied.apply(self.endpoint.api.session)
        if 'timeout' in data:
            self.timeout_applied = data['timeout']
            self.endpoint.api.timeout = data['timeout']
        if 'verify' in data:
            self.verify_applied = data['verify']
            self.endpoint.api.verify = data['verify']

    def set_method(self, method):
        '''Override request method'''
        self.method = method

    def set_timeout(self, timeout):
        '''Override endpoints timeout'''
        self.timeout_applied = timeout
        self.endpoint.api.timeout = timeout

    def update_kwargs(self, kwargs):
        '''Update kwargs (add or modify)'''
        self.kwargs.update(kwargs)

    def set_kwargs(self, kwargs):
        '''Set a new key-value pairs by removing old one'''
        self.kwargs = kwargs

    def set_auth(self, auth_id):
        '''Override endpoints authentication'''
        self.auth_applied = self.workspace.get_auth(auth_id)
        self.auth_applied.apply(self.endpoint.api.session)

    def set_headers(self, headers_id):
        '''Override endpoints headers'''
        self.headers_applied = self.workspace.get_headers(headers_id)
        self.headers_applied.apply(
            self.endpoint.api.session)

    def add_slug(self, slug):
        '''Add slug to current endpoint'''
        self.endpoint.api = self.endpoint.api.route(slug)

    def set_debug(self, value):
        '''Enable/disable debug mode'''
        self.endpoint.api.debug = value

    def do(self):
        '''Invoke the query'''
        return self.endpoint.do(method=self.method, kwargs=self.kwargs)

    def dict(self):
        '''Return information about request in dict format'''
        request = {
            'method': self.method,
            'site': self.endpoint.site.site_id,
            'endpoint': self.endpoint.endpoint_id,
            'kwargs': self.kwargs,
        }
        if self.auth_applied is not None:
            request.update({'auth': self.auth_applied.auth_id})
        if self.headers_applied is not None:
            request.update({'headers': self.headers_applied.headers_id})
        if self.timeout_applied is not None:
            request.update({'timeout': self.timeout_applied})
        if self.verify_applied is not None:
            request.update({'verify': self.verify_applied})

        return request

    def save_as(self, request_id):
        '''Save the query for later use'''

        fileinfo = self.workspace.saved_requests_file

        locked_file = LockedReadWriter(logger=self.workspace.logger).open(fileinfo.path)
        data = locked_file.read()

        data['saved_requests'].update({request_id: self.dict()})
        locked_file.write(data=data)
        locked_file.close()

    def __repr__(self):
        return self.dict()
