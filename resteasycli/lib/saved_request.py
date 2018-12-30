class SavedRequest(object):
    '''Saved requests for reuse and lazyness'''

    def __init__(self, request_id, workspace):
        self.request_id = request_id
        self.workspace = workspace
        data = workspace.saved_requests[request_id]
        self.method = data['method']
        self.endpoint = workspace.get_site(
            data['site']).get_endpoint(data['endpoint'])
        self.kwargs = data.get('kwargs', {})
        if 'auth' in data:
            workspace.get_auth(data['auth']).apply(self.endpoint.api.session)
        if 'headers' in data:
            workspace.get_headers(data['headers']).apply(
                self.endpoint.api.session)
        if 'timeout' in data:
            self.endpoint.api.timeout = data['timeout']
    
    def set_method(self, method):
        '''Override request method'''
        self.method = method

    def set_timeout(self, timeout):
        '''Override endpoints timeout'''
        self.endpoint.api.timeout = timeout
    
    def update_kwargs(self, kwargs):
        '''Update kwargs (add or modify)'''
        self.kwargs.update(kwargs)

    def set_kwargs(self, kwargs):
        '''Set a new key-value pairs by removing old one'''
        self.kwargs = kwargs

    def set_auth(self, auth_id):
        '''Override endpoints authentication'''
        self.workspace.get_auth(auth_id).apply(self.endpoint.api.session)
    
    def set_headers(self, headers_id):
        '''Override endpoints headers'''
        self.workspace.get_headers(headers_id).apply(
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
