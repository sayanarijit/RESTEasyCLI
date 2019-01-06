import os


class DefaultConfig(object):
    '''Default configuration'''

    VERSION = 'v0.4.0' # Also update setup.py
    DESCRIPTION = 'Handy REST API client on your terminal'

    ALL_METHODS = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')
    DEFAULT_ALLOWED_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']

    SEARCH_PATHS = ['.', '~/.recli', '/etc/recli']

    SUPPORTED_FILE_FORMATS = ('v0.1', 'v1.0')
    DEFAULT_FILE_FORMAT = 'v1.0'
    SUPPORTED_FILE_EXTENSIONS = ('json', 'yml', 'yaml')
    DEFAULT_FILE_EXTENSION = 'yml'

    SITES_TEMPLATE_FILENAME = 'sites'
    AUTH_TEMPLATE_FILENAME = 'auth'
    HEADERS_TEMPLATE_FILENAME = 'headers'
    SAVED_REQUESTS_TEMPLATE_FILENAME = 'saved'

    WORKSPACE_TITLE = os.path.basename(
        os.path.basename(os.path.abspath('.')))
    WORKSPACE_DESCRIPTION = ''
