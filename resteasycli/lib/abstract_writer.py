import json

from resteasycli.config import Config
from resteasycli.lib.utils import yaml, Dumper
from resteasycli.exceptions import FileExtensionNotSupportedException


def _write_json(data, filepath):
    '''Write json files'''
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

def _write_yaml(data, filepath):
    '''Write yaml files'''
    with open(filepath, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, Dumper=Dumper)


class Writer(object):
    '''Interface for writing to all supported file formats'''

    SUPPORTED_FILE_EXTENSIONS = Config.SUPPORTED_FILE_EXTENSIONS

    def __init__(self, logger):
        self.logger = logger

    def load_writer_by_extension(self, ext):
        '''Initialize write() interface based on file extension'''

        ext = ext.lower()

        if ext not in self.SUPPORTED_FILE_EXTENSIONS:
            raise FileExtensionNotSupportedException(
                'extension not supported: ' + ext)

        if ext == 'json':
            self.write = _write_json
        else:
            self.write = _write_yaml
