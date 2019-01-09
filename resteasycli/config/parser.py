import os


class Parser(object):
    '''Helps parsing configuration file'''

    def __init__(self):
        self._parsed = dict()

    def parse(self, search_paths):
        '''Fing and return dict object containing configurations'''
        filepath = self.find(search_paths)
        if not filepath:
            return {}

        with open(filepath) as f:
            lines = f.read().splitlines()

        line_no = 0
        for line in lines:
            line_no += 1
            line = line.strip()
            if not line or line.startswith('#') or line.startswith(';'):
                continue
            if '=' not in line:
                raise RuntimeError('file: {}: line no: {}: correct format is: key = value'.format(
                    filepath, line_no
                ))
            if "'" in line or '"' in line:
                raise RuntimeError(
                    'file: {}: line no: {}: do not use quotes'.format(filepath, line_no))
            key, val = line.split('=', 1)
            key, val = key.strip(), val.strip()
            if not key:
                raise RuntimeError(
                    'file: {}: line no: {}: key is missing'.format(filepath, line_no))

            if key in ['DEFAULT_ALLOWED_METHODS', 'SEARCH_PATHS']:
                self._parsed.update({key: [x.strip() for x in val.split(',')]})
                continue

            if val and key in ['DEFAULT_TIMEOUT']:
                self._parsed.update({key: int(val)})
                continue

            if val and key in [
                    'DEFAULT_FILE_FORMAT', 'DEFAULT_FILE_EXTENSION',
                    'SITES_TEMPLATE_FILENAME', 'DEFAULT_SITE_ID',
                    'AUTH_TEMPLATE_FILENAME', 'HEADERS_TEMPLATE_FILENAME',
                    'SAVED_REQUESTS_TEMPLATE_FILENAME', 'WORKSPACE_TITLE',
                    'WORKSPACE_DESCRIPTION', 'DEFAULT_ENDPOINT_ID',
                    'DEFAULT_HEADERS_ID', 'DEFAULT_AUTH_ID',
                    'DEFAULT_CERTFILE', 'DEFAULT_OUTPUT_FORMAT']:
                self._parsed.update({key: val})
                continue

        return self._parsed

    def find(self, search_paths):
        '''Helps finding the file'''
        for path in search_paths:
            filepath = os.path.join(path, 'recli.cfg')
            if not os.path.exists(filepath):
                continue
            return filepath
