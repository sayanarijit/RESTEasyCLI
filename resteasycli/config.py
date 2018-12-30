import os

class Config(object):
    VERSION = 'v0.2.0'
    DESCRIPTION = 'Handy REST API client on your terminal'
    SUPPORTED_EXTENSIONS = os.environ.get(
        'RECLI_SUPPORTED_EXTENSIONS', 'json,yml,yaml').split(',')
    SEARCH_PATHS = os.environ.get(
        'RECLI_SEARCH_PATHS', '.,~/.recli,/etc/recli').split(',')
    DEFAULT_ALLOWED_METHODS = os.environ.get(
        'RECLI_DEFAULT_ALLOWED_METHODS', 'GET,POST,PUT,PATCH,DELETE').split(',')
    SITES_TEMPLATE_FILENAME = os.environ.get('RECLI_SITES_TEMPLATE_FILENAME', 'sites.yml')
    AUTH_TEMPLATE_FILENAME=os.environ.get('RECLI_AUTH_TEMPLATE_FILENAME', 'auth.yml')
    HEADERS_TEMPLATE_FILENAME = os.environ.get(
        'RECLI_HEADERS_TEMPLATE_FILENAME', 'headers.yml')
    SAVED_REQUESTS_TEMPLATE_FILENAME = os.environ.get(
        'RECLI_SAVED_REQUESTS_TEMPLATE_FILENAME', 'saved.yml')
