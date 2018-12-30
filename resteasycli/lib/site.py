from resteasy import RESTEasy

from resteasycli.lib.endpoint import Endpoint

class Site(RESTEasy):
    '''A site is a modified RESTEasy object'''
    def __init__(self, site_id, workspace):
        data = workspace.sites[site_id]
        RESTEasy.__init__(self, base_url=data['base_url'])
        self.workspace = workspace
        self.endpoints = data['endpoints']
        if 'auth' in data:
            workspace.get_auth(data['auth']).apply(self.session)
        if 'headers' in data:
            workspace.get_headers(data['headers']).apply(self.session)
        if 'verify' in data:
            self.session.verify = data['verify']
        if 'timeout' in data:
            self.timeout = data['timeout']

    def get_endpoint(self, endpoint_id, slug=None):
        return Endpoint(endpoint_id=endpoint_id, site=self, slug=slug)
