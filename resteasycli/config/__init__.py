from resteasycli.config.default import DefaultConfig
from resteasycli.config.parser import Parser


parsed = Parser().parse(search_paths=['.', '~/.recli', '/etc/recli'])


class Config(DefaultConfig):
    '''Global configuration object holding default and overridden values'''

    DEFAULT_ALLOWED_METHODS = parsed.get(
        'DEFAULT_ALLOWED_METHODS', DefaultConfig.DEFAULT_ALLOWED_METHODS)

    SEARCH_PATHS = parsed.get(
        'SEARCH_PATHS', DefaultConfig.SEARCH_PATHS)

    DEFAULT_FILE_FORMAT = parsed.get(
        'DEFAULT_FILE_FORMAT', DefaultConfig.DEFAULT_FILE_FORMAT)
    DEFAULT_FILE_EXTENSION = parsed.get(
        'DEFAULT_FILE_EXTENSION', DefaultConfig.DEFAULT_FILE_EXTENSION)

    SITES_TEMPLATE_FILENAME = parsed.get(
        'SITES_TEMPLATE_FILENAME', DefaultConfig.SITES_TEMPLATE_FILENAME)
    AUTH_TEMPLATE_FILENAME = parsed.get(
        'AUTH_TEMPLATE_FILENAME', DefaultConfig.AUTH_TEMPLATE_FILENAME)
    HEADERS_TEMPLATE_FILENAME = parsed.get(
        'HEADERS_TEMPLATE_FILENAME', DefaultConfig.HEADERS_TEMPLATE_FILENAME)
    SAVED_REQUESTS_TEMPLATE_FILENAME = parsed.get(
        'SAVED_REQUESTS_TEMPLATE_FILENAME', DefaultConfig.SAVED_REQUESTS_TEMPLATE_FILENAME)

    WORKSPACE_TITLE = parsed.get(
        'WORKSPACE_TITLE', DefaultConfig.WORKSPACE_TITLE)
    WORKSPACE_DESCRIPTION = parsed.get(
        'WORKSPACE_DESCRIPTION', DefaultConfig.WORKSPACE_DESCRIPTION)

    DEFAULT_OUTPUT_FORMAT = parsed.get(
        'DEFAULT_OUTPUT_FORMAT', DefaultConfig.DEFAULT_OUTPUT_FORMAT)

    DEFAULT_SITE_ID = parsed.get(
        'DEFAULT_SITE_ID', DefaultConfig.DEFAULT_SITE_ID)
    DEFAULT_ENDPOINT_ID = parsed.get(
        'DEFAULT_ENDPOINT_ID', DefaultConfig.DEFAULT_ENDPOINT_ID)
    DEFAULT_HEADERS_ID = parsed.get(
        'DEFAULT_HEADERS_ID', DefaultConfig.DEFAULT_HEADERS_ID)
    DEFAULT_AUTH_ID = parsed.get(
        'DEFAULT_AUTH_ID', DefaultConfig.DEFAULT_AUTH_ID)
    DEFAULT_TIMEOUT = parsed.get(
        'DEFAULT_TIMEOUT', DefaultConfig.DEFAULT_TIMEOUT)
    DEFAULT_CERTFILE = parsed.get(
        'DEFAULT_CERTFILE', DefaultConfig.DEFAULT_CERTFILE)
