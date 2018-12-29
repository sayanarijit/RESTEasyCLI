from resteasy import RESTEasy

from resteasycli.lib.endpoint import Endpoint


class Site(RESTEasy):
    '''A site is a modified RESTEasy object'''
    def __init__(self, data):
        RESTEasy.__init__(self, base_url=data['base_url'])
        if 'auth' in data:
            self.session.auth = (data['username'], data['password'])
        if 'verify' in data:
            self.session.verify = data['verify']
        if 'headers' in data:
            self.session.headers = data['headers']
        if 'timeout' in data:
            self.timeout = data['timeout']

    def get_endpoint(self, endpoint_data, slug=None):
        return Endpoint(site=self, data=endpoint_data, slug=slug)
