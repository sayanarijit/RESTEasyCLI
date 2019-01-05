import json

from resteasycli.config import Config
from resteasycli.lib.utils import yaml, Loader
from resteasycli.exceptions import FileExtensionNotSupportedException


def _read_json(filepath):
    '''Read json files'''
    with open(filepath) as f:
        data = json.load(f)
    return data

def _read_yaml(filepath):
    '''Read yaml files'''
    with open(filepath) as f:
        data = yaml.load(f, Loader=Loader)
    return data


class Reader(object):
    '''Interface for reading all supported file formats'''

    SUPPORTED_FILE_EXTENSIONS = Config.SUPPORTED_FILE_EXTENSIONS

    def __init__(self, logger):
        self.logger = logger

    def load_reader_by_extension(self, ext):
        '''Initialize read() interface based on file extension'''

        ext = ext.lower()

        if ext not in self.SUPPORTED_FILE_EXTENSIONS:
            raise FileExtensionNotSupportedException('extension not supported: ' + ext)

        if ext == 'json':
            self.read = _read_json
        else:
            self.read = _read_yaml
