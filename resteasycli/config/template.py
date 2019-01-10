import os
from resteasycli.config.default import DefaultConfig


CONFIG_TEMPLATE_CONTENT = '''\
### Configuration file for RESTEasyCLI
### Values mentioned here are default values
### Uncomment lines and edit values as required

### Request methods to allow (e.g. {allowed_methods})
# DEFAULT_ALLOWED_METHODS = {default_allowed_methods}

### Where to search for workspace files (priority highest -> lowest)
# SEARCH_PATHS = {search_paths}

### Which file format to use for initializing workspace files (e.g. {file_formats})
# DEFAULT_FILE_FORMAT = {default_file_format}

### Which file extension to use for initializing workspace files (e.g. {file_extensions})
# DEFAULT_FILE_EXTENSION = {default_file_extension}

### Name of the sites template file
# SITES_TEMPLATE_FILENAME = {sites_template_filename}

### Name of the auth template file
# AUTH_TEMPLATE_FILENAME = {auth_template_filename}

### Name of the headers template file
# HEADERS_TEMPLATE_FILENAME = {headers_template_filename}

### Name of the saved requests template file
# SAVED_REQUESTS_TEMPLATE_FILENAME = {saved_requests_template_filename}

### Default output format (e.g. {output_formats})
# DEFAULT_OUTPUT_FORMAT = {default_output_format}

### Title for current workspace
# WORKSPACE_TITLE = {workspace_title}

### Description for current workspace
# WORKSPACE_DESCRIPTION =

### Default values to provide when no command-line argument is provided
# DEFAULT_SITE_ID =
# DEFAULT_ENDPOINT_ID =
# DEFAULT_HEADERS_ID =
# DEFAULT_AUTH_ID =
# DEFAULT_TIMEOUT =
# DEFAULT_CERTFILE =
'''

class ConfigTemplate(object):
    '''Helps initializing configuration template file'''

    @staticmethod
    def initialize(force=False):
        '''Initialize config file in current workspace'''

        if os.path.exists('recli.cfg') and not force:
            return

        with open('recli.cfg', 'w') as f:
            f.write(CONFIG_TEMPLATE_CONTENT.format(
                allowed_methods=(', '.join(DefaultConfig.ALL_METHODS)),
                default_allowed_methods=(', '.join(DefaultConfig.DEFAULT_ALLOWED_METHODS)),
                search_paths=(', '.join(DefaultConfig.SEARCH_PATHS)),
                default_file_format=DefaultConfig.DEFAULT_FILE_FORMAT,
                default_file_extension=DefaultConfig.DEFAULT_FILE_EXTENSION,
                sites_template_filename=DefaultConfig.SITES_TEMPLATE_FILENAME,
                auth_template_filename=DefaultConfig.AUTH_TEMPLATE_FILENAME,
                headers_template_filename=DefaultConfig.HEADERS_TEMPLATE_FILENAME,
                saved_requests_template_filename=DefaultConfig.SAVED_REQUESTS_TEMPLATE_FILENAME,
                workspace_title=DefaultConfig.WORKSPACE_TITLE,
                output_formats=(', '.join(DefaultConfig.SUPPORTED_OUTPUT_FORMATS)),
                default_output_format=DefaultConfig.DEFAULT_OUTPUT_FORMAT,
                file_formats=(', '.join(DefaultConfig.SUPPORTED_FILE_FORMATS)),
                file_extensions=(', '.join(DefaultConfig.SUPPORTED_FILE_EXTENSIONS))
            ))
