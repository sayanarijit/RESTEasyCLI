class Config(object):
    VERSION = 'v0.1.2'
    DESCRIPTION = 'Handy REST API client on your terminal'
    SUPPORTED_EXTENSIONS = ['json', 'yml', 'yaml']
    SEARCH_PATHS = ['.', '~/.recli', '/etc/recli']
    SITE_FILE_NAMES = ['sites']
    DEFAULT_ALLOWED_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    SITE_TEMPLATE_FILENAME = 'sites.yml'
