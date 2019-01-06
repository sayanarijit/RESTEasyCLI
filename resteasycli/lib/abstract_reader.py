from codecs import open

from resteasycli.lib.utils import yaml, Loader
from resteasycli.exceptions import FileExtensionNotSupportedException


def _read_json(filepath):
    '''Read json files'''
    with open(filepath, encoding='utf-8') as f:
        data = yaml.load(f, Loader=Loader)
    return data

def _read_yaml(filepath):
    '''Read yaml files'''
    with open(filepath, encoding='utf-8') as f:
        data = yaml.load(f, Loader=Loader)
    return data


class Reader(object):
    '''Interface for reading all supported file formats'''

    def __init__(self, logger, extensions):
        self.logger = logger
        self.extensions = extensions

    def load_reader_by_extension(self, ext):
        '''Initialize read() interface based on file extension'''

        ext = ext.lower()

        if ext not in self.extensions:
            raise FileExtensionNotSupportedException(
                '{}: extension not supported. Supported extensions are: {}'.format(
                    ext, ', '.join(self.extensions)
                ))

        if ext == 'json':
            self.read = _read_json
        else:
            self.read = _read_yaml
