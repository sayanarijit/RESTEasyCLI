import os

class Config(object):
    VERSION = 'v0.3.5' # Also update setup.py
    DESCRIPTION = 'Handy REST API client on your terminal'
    ALL_METHODS = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    SUPPORTED_EXTENSIONS = os.environ.get(
        'RECLI_SUPPORTED_EXTENSIONS', 'json,yml,yaml').split(',')
    DEFAULT_FILE_EXTENSION = os.environ.get('RECLI_DEFAULT_FILE_EXTENSION', 'yml')
    SEARCH_PATHS = os.environ.get(
        'RECLI_SEARCH_PATHS', '.,~/.recli,/etc/recli').split(',')
    DEFAULT_ALLOWED_METHODS = os.environ.get(
        'RECLI_DEFAULT_ALLOWED_METHODS', 'GET,POST,PUT,PATCH,DELETE').split(',')
    SITES_TEMPLATE_FILENAME = os.environ.get('RECLI_SITES_TEMPLATE_FILENAME', 'sites')
    AUTH_TEMPLATE_FILENAME=os.environ.get('RECLI_AUTH_TEMPLATE_FILENAME', 'auth')
    HEADERS_TEMPLATE_FILENAME = os.environ.get(
        'RECLI_HEADERS_TEMPLATE_FILENAME', 'headers')
    SAVED_REQUESTS_TEMPLATE_FILENAME = os.environ.get(
        'RECLI_SAVED_REQUESTS_TEMPLATE_FILENAME', 'saved')
