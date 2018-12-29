from resteasy import RESTEasy, json

from resteasycli.readers.endpoint_reader import EndpointReader

class EndpointsLoader(object):
    '''Loads endpoints from dict'''
    self.endpoints = {}
    self.

def main():
    '''Entrypoint to the app'''
    args = {'site': 'github_jobs', 'route': ['positions'], 'template': 'fulltime_python_jobs'}
    endp = EndpointReader().read([args['site']])

    api = RESTEasy(base_url=enpargs.site)
