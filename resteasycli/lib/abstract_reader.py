import yaml
import json

from resteasycli.exceptions import FileExtensionNotSupportedException
from resteasycli.config import Config


def _read_json(filepath):
    '''Read json files'''
    with open(filepath) as f:
        data = json.load(f)
    return data

def _read_yaml(filepath):
    '''Read yaml files'''
    with open(filepath) as f:
        data = yaml.load(f.read())
    return data


class Reader(object):
    '''Interface for reading all supported file formats'''

    SUPPORTED_EXTENSIONS = Config.SUPPORTED_EXTENSIONS

    def __init__(self, logger):
        self.logger = logger

    def load_reader_by_extension(self, ext):
        '''Initialize read() interface based on file extension'''

        ext = ext.lower()

        if ext not in self.SUPPORTED_EXTENSIONS:
            raise FileExtensionNotSupportedException('extension not supported: ' + ext)

        if ext == 'json':
            self.read = _read_json
        else:
            self.read = _read_yaml
